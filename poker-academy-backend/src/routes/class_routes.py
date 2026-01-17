# src/routes/class_routes.py
import sys
import os

# Adiciona o diretório pai de 'src' (ou seja, 'poker_academy_api') ao sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, current_app, send_from_directory
from src.models import db, Classes, UserProgress, ClassViews, Users, UserType
from src.auth import token_required, admin_required, AuthService
from datetime import datetime
from sqlalchemy import desc
import os
import re
from werkzeug.utils import secure_filename

class_bp = Blueprint("class_bp", __name__)

# Configuracao de upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'uploads', 'videos')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'}

# Criar pasta de uploads se nao existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Categorias validas
VALID_CATEGORIES = ['iniciantes', 'preflop', 'postflop', 'mental', 'icm']

def normalize_category(category_name):
    """
    Normaliza nomes de categoria em portugues para valores padronizados.
    Retorna uma string com o valor da categoria.
    """
    if not category_name:
        return 'preflop'

    normalized = category_name.lower().strip()

    # Mapeamento de nomes em portugues para valores padronizados
    category_map = {
        'iniciantes': 'iniciantes',
        'iniciante': 'iniciantes',
        'preflop': 'preflop',
        'pre-flop': 'preflop',
        'pré-flop': 'preflop',
        'postflop': 'postflop',
        'pos-flop': 'postflop',
        'pós-flop': 'postflop',
        'posflop': 'postflop',
        'mental': 'mental',
        'mental game': 'mental',
        'mental games': 'mental',
        'mentalg': 'mental',
        'icm': 'icm',
        'geral': 'preflop'
    }

    return category_map.get(normalized, 'preflop')

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
    """
    Cria uma nova aula.

    Request JSON:
        {
            "name": "Nome da aula",
            "instructor_id": 1,  // ID do instrutor
            "date": "2025-01-14",
            "category": "preflop",  // opcional
            "video_url": "https://pub-xxx.r2.dev/videos/...",
            "priority": 5  // opcional
        }
    """
    data = request.get_json()
    print(f"🔍 Dados recebidos para criar aula: {data}")

    if not data:
        return jsonify(error="Dados nao fornecidos"), 400

    # Campos obrigatorios
    required_fields = ["name", "instructor_id", "date"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify(error=f"Campo obrigatorio ausente ou vazio: {field}"), 400

    try:
        # Converter data string para objeto date
        date_obj = datetime.strptime(data["date"], "%Y-%m-%d").date()

        # Normalizar categoria
        category = normalize_category(data.get("category"))

        new_class = Classes(
            name=data["name"],
            instructor_id=data["instructor_id"],
            date=date_obj,
            category=category,
            video_url=data.get("video_url"),
            video_duration=data.get("video_duration"),
            priority=data.get("priority", 5),
            views=0
        )
        db.session.add(new_class)
        db.session.commit()

        print(f"✅ Aula criada: {new_class.name} (ID: {new_class.id})")
        return jsonify(new_class.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar classe: {e}", exc_info=True)
        return jsonify(error=f"Erro ao criar nova aula: {str(e)}"), 500


@class_bp.route("/api/classes/<int:class_id>", methods=["PUT"])
@admin_required
def update_class(current_user, class_id):
    """
    Atualiza uma aula existente.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify(error="Dados nao fornecidos"), 400

        cls_to_update = Classes.query.get(class_id)
        if not cls_to_update:
            return jsonify(error="Aula nao encontrada"), 404

        # Campos que podem ser atualizados
        if "name" in data:
            cls_to_update.name = data["name"]
        if "instructor_id" in data:
            cls_to_update.instructor_id = data["instructor_id"]
        if "date" in data:
            cls_to_update.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        if "category" in data:
            cls_to_update.category = normalize_category(data["category"])
        if "video_url" in data:
            cls_to_update.video_url = data["video_url"]
        if "video_duration" in data:
            cls_to_update.video_duration = data["video_duration"]
        if "priority" in data:
            cls_to_update.priority = data["priority"]

        db.session.commit()
        print(f"✅ Aula atualizada: {cls_to_update.name} (ID: {class_id})")
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

        # Buscar todas as visualizações da aula com dados do aluno
        views = db.session.query(ClassViews, Users).join(
            Users, ClassViews.user_id == Users.id
        ).filter(
            ClassViews.class_id == class_id
        ).order_by(desc(ClassViews.viewed_at)).all()

        # Estatísticas
        total_views = len(views)
        unique_users = len(set(view.user_id for view, user in views))

        # Montar lista de views com dados do aluno
        views_list = []
        for view, user in views:
            view_dict = view.to_dict()
            view_dict['student_name'] = user.name
            view_dict['student_email'] = user.email
            views_list.append(view_dict)

        result = {
            'class_id': class_id,
            'class_name': class_obj.name,
            'total_views': total_views,
            'unique_users': unique_users,
            'views': views_list
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
                'username': instructor.username,
                'email': instructor.email
            })

        return jsonify(result), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar instrutores: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar instrutores"), 500

# Rota para criar novo instrutor (admin)
@class_bp.route("/api/instructors", methods=["POST"])
@admin_required
def create_instructor(current_user):
    try:
        data = request.get_json()

        # Validar campos obrigatórios
        if not data.get('name') or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify(error="Nome, username, email e senha são obrigatórios"), 400

        # Verificar se email já existe
        existing_email = Users.query.filter_by(email=data['email']).first()
        if existing_email:
            return jsonify(error="Email já cadastrado"), 400

        # Verificar se username já existe
        existing_username = Users.query.filter_by(username=data['username']).first()
        if existing_username:
            return jsonify(error="Username já cadastrado"), 400

        # Usar a mesma partição do admin atual
        particao_id = current_user.particao_id

        # Criar novo instrutor (admin)
        hashed_password = AuthService.hash_password(data['password'])
        new_instructor = Users(
            name=data['name'],
            username=data['username'],
            email=data['email'],
            password_hash=hashed_password,
            type=UserType.admin,
            particao_id=particao_id
        )

        db.session.add(new_instructor)
        db.session.commit()

        return jsonify({
            'message': 'Instrutor criado com sucesso',
            'instructor': {
                'id': new_instructor.id,
                'name': new_instructor.name,
                'username': new_instructor.username,
                'email': new_instructor.email
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar instrutor: {e}", exc_info=True)
        return jsonify(error="Erro ao criar instrutor"), 500

# Rota para atualizar instrutor (admin)
@class_bp.route("/api/instructors/<int:instructor_id>", methods=["PUT"])
@admin_required
def update_instructor(current_user, instructor_id):
    try:
        instructor = Users.query.filter_by(id=instructor_id, type=UserType.admin).first()
        if not instructor:
            return jsonify(error="Instrutor não encontrado"), 404

        data = request.get_json()

        # Atualizar campos
        if data.get('name'):
            instructor.name = data['name']

        if data.get('username'):
            # Verificar se username já existe para outro usuário
            existing_username = Users.query.filter(Users.username == data['username'], Users.id != instructor_id).first()
            if existing_username:
                return jsonify(error="Username já cadastrado para outro usuário"), 400
            instructor.username = data['username']

        if data.get('email'):
            # Verificar se email já existe para outro usuário
            existing_email = Users.query.filter(Users.email == data['email'], Users.id != instructor_id).first()
            if existing_email:
                return jsonify(error="Email já cadastrado para outro usuário"), 400
            instructor.email = data['email']

        if data.get('password'):
            instructor.password_hash = AuthService.hash_password(data['password'])

        db.session.commit()

        return jsonify({
            'message': 'Instrutor atualizado com sucesso',
            'instructor': {
                'id': instructor.id,
                'name': instructor.name,
                'username': instructor.username,
                'email': instructor.email
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar instrutor: {e}", exc_info=True)
        return jsonify(error="Erro ao atualizar instrutor"), 500

# Rota para excluir instrutor (admin)
@class_bp.route("/api/instructors/<int:instructor_id>", methods=["DELETE"])
@admin_required
def delete_instructor(current_user, instructor_id):
    try:
        instructor = Users.query.filter_by(id=instructor_id, type=UserType.admin).first()
        if not instructor:
            return jsonify(error="Instrutor não encontrado"), 404

        # Não permitir excluir a si mesmo
        if instructor.id == current_user.id:
            return jsonify(error="Você não pode excluir sua própria conta"), 400

        # Verificar se instrutor tem aulas associadas
        classes_count = Classes.query.filter_by(instructor_id=instructor_id).count()
        if classes_count > 0:
            return jsonify(error=f"Não é possível excluir. Este instrutor possui {classes_count} aula(s) associada(s)"), 400

        db.session.delete(instructor)
        db.session.commit()

        return jsonify({'message': 'Instrutor excluído com sucesso'}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao excluir instrutor: {e}", exc_info=True)
        return jsonify(error="Erro ao excluir instrutor"), 500

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
        classes_with_video = Classes.query.filter(Classes.video_url.isnot(None)).count()

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

# Rota para servir vídeos do diretório uploads (nova estrutura)
@class_bp.route("/api/uploads/videos/<filename>")
def serve_uploaded_video(filename):
    """Serve vídeos do diretório uploads/videos com autenticação via query parameter"""
    try:
        # Verificar autenticação via query parameter ou header
        token = request.args.get('token') or request.headers.get('Authorization')

        if not token:
            return jsonify(error="Token de acesso necessário"), 401

        # Se o token vem do header, remover 'Bearer '
        if token.startswith('Bearer '):
            token = token[7:]

        # Verificar se o token é válido
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
        response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', 'http://localhost:3000')
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    except Exception as e:
        current_app.logger.error(f"Erro ao servir vídeo do uploads: {e}", exc_info=True)
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
        # Normalizar categoria recebida
        print(f"📂 Categoria recebida: '{category}'")

        # Normalizar a categoria
        final_category = normalize_category(category)
        print(f"✅ Categoria normalizada: '{final_category}'")

        # Buscar o ID do instrutor pelo nome
        instructor_user = Users.query.filter_by(name=instructor).first()
        if not instructor_user:
            raise ValueError(f"Instrutor {instructor} não encontrado no banco de dados")
        
        # Criar a aula com categoria garantidamente válida
        try:
            new_class = Classes(
                name=name,
                instructor_id=instructor_user.id,
                date=date_obj,
                category=final_category,
                video_url=f"/api/uploads/videos/{filename}",
                priority=int(priority),
                views=0
            )
            db.session.add(new_class)
            db.session.commit()

            print(f"✅ Aula criada com sucesso! ID={new_class.id}, Categoria='{final_category}'")

        except Exception as create_error:
            db.session.rollback()
            print(f"❌ Erro ao criar aula: {create_error}")
            raise create_error

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

# Rota para obter categorias disponíveis
@class_bp.route("/api/classes/categories", methods=["GET"])
@token_required
def get_categories(current_user):
    """
    Retorna todas as categorias disponíveis no ENUM
    """
    try:
        # Obter valores atuais do ENUM
        result = db.session.execute(db.text("SHOW COLUMNS FROM classes LIKE 'category'")).fetchone()
        current_enum = result[1]  # Type column

        # Extrair valores atuais do ENUM
        import re
        enum_values = re.findall(r"'([^']*)'", current_enum)

        print(f"📋 Categorias disponíveis: {enum_values}")

        return jsonify({
            'categories': enum_values
        }), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar categorias: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar categorias"), 500

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

                # Buscar instrutor pelo nome
                instructor_user = Users.query.filter_by(name=class_data["instructor"]).first()
                if not instructor_user:
                    errors.append(f"Instrutor '{class_data['instructor']}' nao encontrado")
                    continue

                # Criar nova aula
                new_class = Classes(
                    name=class_data["name"],
                    instructor_id=instructor_user.id,
                    date=date_obj,
                    category=None,
                    video_url=None,
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

