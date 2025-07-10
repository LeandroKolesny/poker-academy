# src/routes/class_routes.py
import sys
import os

# Adiciona o diretório pai de 'src' (ou seja, 'poker_academy_api') ao sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, current_app, send_from_directory
from src.models import db, Classes, UserProgress, ClassViews, Users, UserType
from src.auth import token_required, admin_required
from datetime import datetime
from sqlalchemy import desc
import os
import re
from werkzeug.utils import secure_filename

class_bp = Blueprint("class_bp", __name__)

# Configurações de upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads', 'videos')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'}

# Criar pasta de upload se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print(f"Pasta de upload: {UPLOAD_FOLDER}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rota de teste sem autenticação
@class_bp.route("/api/test", methods=["GET"])
def test_route():
    try:
        print("🧪 Rota de teste chamada!")

        # Testar conexão com banco
        all_classes = Classes.query.all()
        print(f"📊 Total de aulas: {len(all_classes)}")

        return jsonify({
            "status": "OK",
            "message": "Backend funcionando",
            "total_classes": len(all_classes)
        }), 200
    except Exception as e:
        print(f"❌ Erro na rota de teste: {e}")
        return jsonify(error=str(e)), 500

# Rota para listar todas as aulas
@class_bp.route("/api/classes", methods=["GET"])
@token_required
def get_all_classes(current_user):
    try:
        print("🔍 Buscando aulas...")

        # Buscar todas as aulas (agora todas têm vídeo)
        all_classes = Classes.query.all()
        print(f"📊 Total de aulas: {len(all_classes)}")

        result = [c.to_dict() for c in all_classes]
        print(f"✅ Retornando {len(result)} aulas")

        return jsonify(result), 200
    except Exception as e:
        print(f"❌ Erro ao buscar aulas: {e}")
        current_app.logger.error(f"Erro ao buscar classes: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar dados das aulas."), 500

# Rota para buscar detalhes de uma aula específica
@class_bp.route("/api/classes/<int:class_id>", methods=["GET"])
def get_class_details(class_id):
    try:
        single_class = Classes.query.get(class_id)
        if not single_class:
            return jsonify(error="Aula não encontrada"), 404
        return jsonify(single_class.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar detalhes da aula {class_id}: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar dados da aula."), 500

# Rota para criar uma nova aula (apenas admin)
@class_bp.route("/api/classes", methods=["POST"])
@admin_required
def create_class(current_user):
    data = request.get_json()
    print(f"🔍 Dados recebidos para criar aula: {data}")

    if not data:
        return jsonify(error="Dados não fornecidos"), 400

    # Campos obrigatórios básicos
    required_fields = ["name", "instructor", "date", "category", "video_type"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify(error=f"Campo obrigatório ausente ou vazio: {field}"), 400

    # Validação específica para vídeo (apenas para novas aulas)
    if not data.get("video_path"):
        return jsonify(error="É obrigatório fazer upload de um vídeo"), 400

    try:
        # Converter data string para objeto date
        from datetime import datetime
        date_obj = datetime.strptime(data["date"], "%Y-%m-%d").date()

        new_class = Classes(
            name=data["name"],
            instructor=data["instructor"],
            date=date_obj,
            category=data.get("category"),  # Categoria agora é opcional
            video_type=data.get("video_type", "local"),
            video_path=data.get("video_path"),
            priority=data.get("priority", 5),
            views=data.get("views", 0)
        )
        db.session.add(new_class)
        db.session.commit()
        return jsonify(new_class.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar classe: {e}", exc_info=True)
        return jsonify(error=f"Erro ao criar nova aula: {str(e)}"), 500


@class_bp.route("/api/classes/<int:class_id>", methods=["PUT"])
def update_class(class_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify(error="Dados não fornecidos"), 400

        cls_to_update = Classes.query.get(class_id)
        if not cls_to_update:
            return jsonify(error="Aula não encontrada"), 404

        # Campos que podem ser atualizados
        if "name" in data:
            cls_to_update.name = data["name"]
        if "instructor" in data:
            cls_to_update.instructor = data["instructor"]
        if "date" in data:
            # Converter data string para objeto date
            from datetime import datetime
            cls_to_update.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        if "category" in data:
            cls_to_update.category = data["category"]
        if "video_type" in data:
            cls_to_update.video_type = data["video_type"]
        if "video_path" in data: # Adicionado para consistência
            cls_to_update.video_path = data["video_path"]
        if "priority" in data:
            cls_to_update.priority = data["priority"]
        
        db.session.commit()
        return jsonify(cls_to_update.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar aula {class_id}: {e}", exc_info=True)
        return jsonify(error=f"Erro ao atualizar aula: {str(e)}"), 500

# Rota para excluir uma aula
@class_bp.route("/api/classes/<int:class_id>", methods=["DELETE"])
def delete_class(class_id):
    cls_to_delete = Classes.query.get(class_id)
    if not cls_to_delete:
        return jsonify(error="Aula não encontrada"), 404

    try:
        print(f"🗑️ Excluindo registros relacionados à aula {class_id}...")

        # Usar SQL direto para excluir registros relacionados
        # 1. Excluir visualizações da aula
        result1 = db.session.execute(db.text("DELETE FROM class_views WHERE class_id = :class_id"), {"class_id": class_id})
        print(f"   ✅ Removidas {result1.rowcount} visualizações")

        # 2. Excluir favoritos da aula
        result2 = db.session.execute(db.text("DELETE FROM favorites WHERE class_id = :class_id"), {"class_id": class_id})
        print(f"   ✅ Removidos {result2.rowcount} favoritos")

        # 3. Excluir aula das playlists
        result3 = db.session.execute(db.text("DELETE FROM playlist_classes WHERE class_id = :class_id"), {"class_id": class_id})
        print(f"   ✅ Removida de {result3.rowcount} playlists")

        # 4. Excluir progresso dos usuários
        result4 = db.session.execute(db.text("DELETE FROM user_progress WHERE class_id = :class_id"), {"class_id": class_id})
        print(f"   ✅ Removido progresso de {result4.rowcount} usuários")

        # 5. Finalmente, excluir a aula
        db.session.execute(db.text("DELETE FROM classes WHERE id = :class_id"), {"class_id": class_id})

        # Commit todas as alterações
        db.session.commit()

        print(f"✅ Aula {class_id} excluída com sucesso!")
        return jsonify(message="Aula excluída com sucesso"), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao excluir aula {class_id}: {e}", exc_info=True)
        return jsonify(error=f"Erro ao excluir aula: {str(e)}"), 500

# Rota para marcar progresso de uma aula
@class_bp.route("/api/classes/<int:class_id>/progress", methods=["POST"])
@token_required
def update_class_progress(current_user, class_id):
    try:
        data = request.get_json()
        progress = data.get('progress', 0)
        watched = data.get('watched', False)
        video_time = data.get('current_time', 0.0)

        # Verificar se a aula existe
        class_obj = Classes.query.get(class_id)
        if not class_obj:
            return jsonify(error="Aula não encontrada"), 404

        # Buscar ou criar progresso do usuário
        user_progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            class_id=class_id
        ).first()

        if user_progress:
            user_progress.progress = progress
            user_progress.watched = watched
            user_progress.video_time = video_time
            user_progress.last_watched = datetime.utcnow()
        else:
            user_progress = UserProgress(
                user_id=current_user.id,
                class_id=class_id,
                progress=progress,
                watched=watched,
                video_time=video_time,
                last_watched=datetime.utcnow()
            )
            db.session.add(user_progress)

        # Incrementar views se assistiu pela primeira vez
        if watched and (not user_progress or not user_progress.watched):
            class_obj.views += 1
            print(f"Views incrementadas para aula {class_id}: {class_obj.views}")

        db.session.commit()
        return jsonify(message="Progresso atualizado com sucesso"), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar progresso: {e}", exc_info=True)
        return jsonify(error="Erro ao atualizar progresso"), 500

# Rota para obter progresso do usuário
@class_bp.route("/api/classes/<int:class_id>/progress", methods=["GET"])
@token_required
def get_class_progress(current_user, class_id):
    try:
        user_progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            class_id=class_id
        ).first()

        if user_progress:
            return jsonify({
                "progress": user_progress.progress,
                "watched": user_progress.watched,
                "current_time": user_progress.video_time,
                "last_watched": user_progress.last_watched.isoformat() if user_progress.last_watched else None
            }), 200
        else:
            return jsonify({
                "progress": 0,
                "watched": False,
                "current_time": 0.0,
                "last_watched": None
            }), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar progresso: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar progresso"), 500

# Rota para obter histórico de aulas assistidas pelo usuário
@class_bp.route("/api/classes/history", methods=["GET"])
@token_required
def get_user_history(current_user):
    try:
        # Buscar aulas que o usuário já assistiu (com progresso > 0)
        history = db.session.query(UserProgress, Classes).join(
            Classes, UserProgress.class_id == Classes.id
        ).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.progress > 0
        ).order_by(desc(UserProgress.last_watched)).all()

        result = []
        for user_progress, class_obj in history:
            class_data = class_obj.to_dict()
            class_data.update({
                'progress': user_progress.progress,
                'watched': user_progress.watched,
                'current_time': user_progress.video_time,
                'last_watched': user_progress.last_watched.isoformat() if user_progress.last_watched else None
            })
            result.append(class_data)

        return jsonify(result), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar histórico: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar histórico"), 500

# Rota para registrar visualização de aula
@class_bp.route("/api/classes/<int:class_id>/view", methods=["POST"])
@token_required
def register_view(current_user, class_id):
    try:
        # Verificar se a aula existe
        class_obj = Classes.query.get(class_id)
        if not class_obj:
            return jsonify(error="Aula não encontrada"), 404

        # Obter informações da requisição
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
        user_agent = request.headers.get('User-Agent')

        # Registrar a visualização
        new_view = ClassViews(
            user_id=current_user.id,
            class_id=class_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(new_view)

        # Incrementar contador de views na aula
        class_obj.views += 1

        db.session.commit()

        return jsonify({
            'message': 'Visualização registrada com sucesso',
            'total_views': class_obj.views
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao registrar visualização: {e}", exc_info=True)
        return jsonify(error="Erro ao registrar visualização"), 500

# Rota para obter estatísticas de visualizações (apenas admin)
@class_bp.route("/api/classes/<int:class_id>/views", methods=["GET"])
@admin_required
def get_class_views(current_user, class_id):
    try:
        # Verificar se a aula existe
        class_obj = Classes.query.get(class_id)
        if not class_obj:
            return jsonify(error="Aula não encontrada"), 404

        # Buscar todas as visualizações da aula
        views = ClassViews.query.filter_by(class_id=class_id).order_by(desc(ClassViews.viewed_at)).all()

        # Estatísticas
        total_views = len(views)
        unique_users = len(set(view.user_id for view in views))

        result = {
            'class_id': class_id,
            'class_name': class_obj.name,
            'total_views': total_views,
            'unique_users': unique_users,
            'views': [view.to_dict() for view in views]
        }

        return jsonify(result), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar visualizações: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar visualizações"), 500

# Rota de teste para upload
@class_bp.route("/api/classes/upload-test", methods=["GET"])
def upload_test():
    return jsonify(message="Rota de upload funcionando!", upload_folder=UPLOAD_FOLDER)

# Rota para listar instrutores (admins) disponíveis
@class_bp.route("/api/instructors", methods=["GET"])
@admin_required
def get_instructors(current_user):
    try:
        # Buscar todos os usuários admin
        instructors = Users.query.filter_by(type=UserType.admin).all()

        result = []
        for instructor in instructors:
            result.append({
                'id': instructor.id,
                'name': instructor.name,
                'email': instructor.email
            })

        return jsonify(result), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar instrutores: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar instrutores"), 500

# Rota para obter estatísticas do painel de analytics (apenas admin)
@class_bp.route("/api/analytics/stats", methods=["GET"])
@admin_required
def get_analytics_stats(current_user):
    try:
        # Total de alunos (usuários do tipo student)
        total_students = Users.query.filter_by(type=UserType.student).count()

        # Total de aulas
        total_classes = Classes.query.count()

        # Aula mais visualizada
        most_popular_class = Classes.query.order_by(desc(Classes.views)).first()
        most_popular_class_name = most_popular_class.name if most_popular_class else "Nenhuma aula"
        most_popular_class_views = most_popular_class.views if most_popular_class else 0

        # Total de visualizações
        total_views = db.session.query(db.func.sum(Classes.views)).scalar() or 0

        # Aulas com vídeo
        classes_with_video = Classes.query.filter(Classes.video_path.isnot(None)).count()

        # Estudantes que já assistiram pelo menos uma aula
        active_students = db.session.query(UserProgress.user_id).distinct().count()

        return jsonify({
            'total_students': total_students,
            'total_classes': total_classes,
            'most_popular_class': most_popular_class_name,
            'most_popular_class_views': most_popular_class_views,
            'total_views': total_views,
            'classes_with_video': classes_with_video,
            'active_students': active_students
        }), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar estatísticas: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar estatísticas"), 500

# Rota para upload de vídeo (apenas admin)
@class_bp.route("/api/classes/upload-video", methods=["POST"])
@admin_required
def upload_video(current_user):
    print("Rota de upload chamada!")
    try:
        if 'video' not in request.files:
            return jsonify(error="Nenhum arquivo enviado"), 400

        file = request.files['video']
        if file.filename == '':
            return jsonify(error="Nenhum arquivo selecionado"), 400

        if file and allowed_file(file.filename):
            # Gerar nome seguro para o arquivo
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
            filename = timestamp + filename

            # Salvar arquivo
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            return jsonify({
                'message': 'Vídeo enviado com sucesso',
                'filename': filename,
                'path': filepath
            }), 200
        else:
            return jsonify(error="Tipo de arquivo não permitido"), 400

    except Exception as e:
        current_app.logger.error(f"Erro no upload: {e}", exc_info=True)
        return jsonify(error="Erro ao fazer upload do vídeo"), 500

# Rota para servir vídeos (com autenticação via query parameter)
@class_bp.route("/api/videos/<filename>")
def serve_video(filename):
    try:
        # Verificar autenticação via query parameter ou header
        token = request.args.get('token') or request.headers.get('Authorization')

        if not token:
            return jsonify(error="Token de acesso necessário"), 401

        # Se o token vem do header, remover 'Bearer '
        if token.startswith('Bearer '):
            token = token[7:]

        # Verificar se o token é válido (simplificado)
        import jwt
        try:
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify(error="Token inválido"), 401

        # Verificar se o arquivo existe
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify(error="Vídeo não encontrado"), 404

        response = send_from_directory(UPLOAD_FOLDER, filename)
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    except Exception as e:
        current_app.logger.error(f"Erro ao servir vídeo: {e}", exc_info=True)
        return jsonify(error="Erro ao carregar vídeo"), 500

# Rota para servir vídeos com autenticação simplificada
@class_bp.route("/api/videos-public/<filename>")
@token_required
def serve_video_public(current_user, filename):
    try:
        print(f"Usuário {current_user.name} acessando vídeo: {filename}")

        # Verificar se o arquivo existe
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify(error="Vídeo não encontrado"), 404

        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        print(f"Erro ao servir vídeo: {e}")
        current_app.logger.error(f"Erro ao servir vídeo: {e}", exc_info=True)
        return jsonify(error="Erro ao carregar vídeo"), 500

# Rota para upload completo (vídeo + dados da aula)
@class_bp.route("/api/classes/upload-complete", methods=["POST"])
@admin_required
def upload_complete_class(current_user):
    """
    Upload completo: recebe arquivo de vídeo + dados da aula em FormData
    """
    print("🚀 Rota de upload completo chamada!")
    try:
        # Verificar se há arquivo de vídeo
        if 'video' not in request.files:
            return jsonify(error="Nenhum arquivo de vídeo enviado"), 400

        file = request.files['video']
        if file.filename == '':
            return jsonify(error="Nenhum arquivo selecionado"), 400

        if not file or not allowed_file(file.filename):
            return jsonify(error="Tipo de arquivo não permitido"), 400

        # Obter dados do formulário
        name = request.form.get('name')
        instructor = request.form.get('instructor')
        date_str = request.form.get('date')
        category = request.form.get('category', '')  # Categoria opcional
        priority = request.form.get('priority', '5')
        video_type = request.form.get('video_type', 'local')

        print(f"📝 Dados recebidos: name={name}, instructor={instructor}, date={date_str}, category={category}")

        # Validar campos obrigatórios
        if not name or not instructor or not date_str:
            return jsonify(error="Campos obrigatórios: name, instructor, date"), 400

        # Gerar nome seguro para o arquivo
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename

        # Salvar arquivo
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        print(f"💾 Arquivo salvo: {filepath}")

        # Converter data string para objeto date
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            # Tentar formato brasileiro
            try:
                date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
            except ValueError:
                return jsonify(error="Formato de data inválido. Use YYYY-MM-DD"), 400

        # Criar nova aula no banco
        # Se categoria estiver vazia, usar um valor padrão válido do ENUM
        final_category = category if category and category.strip() else 'geral'

        print(f"📂 Categoria recebida: '{category}' -> Categoria final: '{final_category}'")

        # VERIFICAR E CRIAR CATEGORIA ANTES de tentar inserir a aula
        try:
            # Obter valores atuais do ENUM
            result = db.session.execute(db.text("SHOW COLUMNS FROM classes LIKE 'category'")).fetchone()
            current_enum = result[1]  # Type column

            # Extrair valores atuais do ENUM
            import re
            enum_values = re.findall(r"'([^']*)'", current_enum)

            print(f"🔍 Categorias existentes no ENUM: {enum_values}")

            # Verificar se a categoria já existe
            if final_category not in enum_values:
                print(f"🔧 Categoria '{final_category}' não existe. Adicionando ao ENUM...")

                # Adicionar nova categoria ao ENUM
                enum_values.append(final_category)
                new_enum = "enum('" + "','".join(enum_values) + "')"

                # Alterar a coluna para incluir a nova categoria
                alter_sql = f"ALTER TABLE classes MODIFY COLUMN category {new_enum}"
                db.session.execute(db.text(alter_sql))
                db.session.commit()

                print(f"✅ Categoria '{final_category}' adicionada ao ENUM com sucesso!")
                print(f"📋 Novo ENUM: {enum_values}")
            else:
                print(f"✅ Categoria '{final_category}' já existe no ENUM")

            # Agora criar a aula com categoria garantidamente válida
            new_class = Classes(
                name=name,
                instructor=instructor,
                date=date_obj,
                category=final_category,
                video_type=video_type,
                video_path=filename,  # Salvar apenas o nome do arquivo
                priority=int(priority),
                views=0
            )
            db.session.add(new_class)
            db.session.commit()

            print(f"✅ Aula criada com sucesso! ID={new_class.id}, Categoria='{final_category}'")

        except Exception as error:
            db.session.rollback()
            print(f"❌ Erro ao criar aula: {error}")

            # Como último recurso, tentar com categoria padrão
            try:
                print("🔄 Tentando com categoria padrão 'geral'...")
                final_category = 'geral'

                # Verificar se 'geral' existe, se não, criar
                result = db.session.execute(db.text("SHOW COLUMNS FROM classes LIKE 'category'")).fetchone()
                current_enum = result[1]
                enum_values = re.findall(r"'([^']*)'", current_enum)

                if 'geral' not in enum_values:
                    enum_values.append('geral')
                    new_enum = "enum('" + "','".join(enum_values) + "')"
                    alter_sql = f"ALTER TABLE classes MODIFY COLUMN category {new_enum}"
                    db.session.execute(db.text(alter_sql))
                    db.session.commit()

                new_class = Classes(
                    name=name,
                    instructor=instructor,
                    date=date_obj,
                    category=final_category,
                    video_type=video_type,
                    video_path=filename,
                    priority=int(priority),
                    views=0
                )
                db.session.add(new_class)
                db.session.commit()

                print(f"✅ Aula criada com categoria padrão '{final_category}'")

            except Exception as final_error:
                db.session.rollback()
                print(f"❌ Erro final: {final_error}")
                raise final_error

        print(f"✅ Aula criada com sucesso: ID={new_class.id}")

        return jsonify({
            'message': 'Aula criada com sucesso',
            'class': new_class.to_dict(),
            'filename': filename
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro no upload completo: {e}")
        current_app.logger.error(f"Erro no upload completo: {e}", exc_info=True)
        return jsonify(error=f"Erro ao criar aula: {str(e)}"), 500

# Rota para auto-import de aulas
@class_bp.route("/api/classes/auto-import", methods=["POST"])
@admin_required
def auto_import_classes(current_user):
    """
    Auto-import de aulas a partir de arquivo de texto
    Formato esperado: Data - Instrutor - Nome da aula
    Exemplo: 21.01.25 - Eiji - Mystery bounty
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Nenhum arquivo selecionado"}), 400

        # Ler conteúdo do arquivo
        content = file.read().decode('utf-8')
        lines = content.strip().split('\n')

        parsed_classes = []
        errors = []

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:  # Pular linhas vazias
                continue

            try:
                # Parse do formato: Data - Instrutor - Nome da aula
                # Exemplo: 21.01.25 - Eiji - Mystery bounty
                parts = line.split(' - ')

                if len(parts) < 3:
                    errors.append(f"Linha {line_num}: Formato inválido. Use: Data - Instrutor - Nome da aula")
                    continue

                date_str = parts[0].strip()
                instructor = parts[1].strip()
                class_name = ' - '.join(parts[2:]).strip()  # Caso o nome tenha " - "

                # Parse da data (formato: dd.mm.yy ou dd.mm.yyyy)
                date_obj = parse_date(date_str)
                if not date_obj:
                    errors.append(f"Linha {line_num}: Data inválida '{date_str}'. Use formato dd.mm.yy ou dd.mm.yyyy")
                    continue

                # Verificar se instrutor existe
                instructor_exists = Users.query.filter_by(name=instructor, type=UserType.admin).first()
                if not instructor_exists:
                    errors.append(f"Linha {line_num}: Instrutor '{instructor}' não encontrado")
                    continue

                parsed_classes.append({
                    'line': line_num,
                    'date': date_obj.strftime('%Y-%m-%d'),
                    'instructor': instructor,
                    'name': class_name,
                    'original_line': line
                })

            except Exception as e:
                errors.append(f"Linha {line_num}: Erro ao processar - {str(e)}")

        return jsonify({
            "success": True,
            "parsed_classes": parsed_classes,
            "errors": errors,
            "total_lines": len(lines),
            "valid_classes": len(parsed_classes),
            "error_count": len(errors)
        })

    except Exception as e:
        return jsonify({"error": f"Erro ao processar arquivo: {str(e)}"}), 500

# Rota para confirmar import das aulas
@class_bp.route("/api/classes/confirm-import", methods=["POST"])
@admin_required
def confirm_import_classes(current_user):
    """
    Confirma o import das aulas parseadas
    """
    try:
        data = request.get_json()
        classes_to_import = data.get('classes', [])

        if not classes_to_import:
            return jsonify({"error": "Nenhuma aula para importar"}), 400

        imported_classes = []
        errors = []

        for class_data in classes_to_import:
            try:
                # Converter data string para objeto date
                date_obj = datetime.strptime(class_data["date"], "%Y-%m-%d").date()

                # Criar nova aula
                new_class = Classes(
                    name=class_data["name"],
                    instructor=class_data["instructor"],
                    date=date_obj,
                    category=None,  # Categoria vazia por padrão
                    video_type="local",
                    video_path=None,
                    priority=5,
                    views=0
                )

                db.session.add(new_class)
                imported_classes.append({
                    'name': class_data["name"],
                    'instructor': class_data["instructor"],
                    'date': class_data["date"]
                })

            except Exception as e:
                errors.append(f"Erro ao importar '{class_data.get('name', 'N/A')}': {str(e)}")

        if imported_classes:
            db.session.commit()

        return jsonify({
            "success": True,
            "imported_count": len(imported_classes),
            "imported_classes": imported_classes,
            "errors": errors
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao importar aulas: {str(e)}"}), 500

def parse_date(date_str):
    """
    Parse de data nos formatos: dd.mm.yy ou dd.mm.yyyy
    Retorna objeto date ou None se inválido
    """
    try:
        # Tentar formato dd.mm.yyyy
        if len(date_str.split('.')) == 3:
            day, month, year = date_str.split('.')

            # Se ano tem 2 dígitos, assumir 20xx
            if len(year) == 2:
                year = '20' + year

            return datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y").date()

        return None
    except:
        return None

