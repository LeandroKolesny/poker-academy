# src/routes/graphs_routes.py
# Updated: 2025-10-16 22:16:00 - Fixing StudentGraphs relationship issue
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from ..models import db, Users, StudentGraphs, StudentLeaks, MonthEnum
from ..auth import token_required

graphs_bp = Blueprint('graphs', __name__)

# Configurações de upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_upload_folder():
    """Retorna o diretório de upload para gráficos"""
    upload_folder = os.path.join(current_app.config.get('UPLOAD_FOLDER', '/app/uploads'), 'graphs')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

@graphs_bp.route('/api/student/graphs', methods=['GET'])
@token_required
def get_student_graphs(current_user):
    """Buscar gráficos do aluno logado"""
    try:
        print(f"\n{'='*80}")
        print(f"🔍 INICIANDO get_student_graphs")
        print(f"{'='*80}")
        print(f"🔍 Verificando se StudentGraphs tem atributo 'student'...")
        print(f"   StudentGraphs.__dict__: {StudentGraphs.__dict__.keys()}")
        print(f"   StudentGraphs.__mapper__.columns: {list(StudentGraphs.__mapper__.columns.keys())}")
        print(f"   StudentGraphs.__mapper__.relationships: {list(StudentGraphs.__mapper__.relationships.keys())}")

        year = request.args.get('year', datetime.now().year, type=int)
        print(f"📅 Year recebido: {year}")
        print(f"👤 Student ID: {current_user.id}")

        # Verificar se StudentGraphs existe
        print(f"🔍 Verificando modelo StudentGraphs...")
        print(f"   Tabela: {StudentGraphs.__tablename__}")

        # Fazer query
        print(f"🔍 Executando query...")
        graphs = StudentGraphs.query.filter_by(
            student_id=current_user.id,
            year=year
        ).all()

        print(f"✅ Gráficos encontrados: {len(graphs)}")

        if len(graphs) == 0:
            print(f"⚠️  Nenhum gráfico encontrado para student_id={current_user.id}, year={year}")

        # Organizar por mês
        graphs_by_month = {}
        for idx, graph in enumerate(graphs):
            try:
                print(f"\n📊 Processando gráfico {idx + 1}/{len(graphs)}")
                print(f"   ID: {graph.id}")
                print(f"   Student ID: {graph.student_id}")
                print(f"   Month: {graph.month}")
                print(f"   Month type: {type(graph.month)}")
                print(f"   Year: {graph.year}")
                print(f"   Image URL: {graph.image_url}")

                # Não tentar acessar o relacionamento aqui
                print(f"   Pulando acesso ao relacionamento (será feito no to_dict)")

                # Converter month para value
                month_value = graph.month.value if hasattr(graph.month, 'value') else graph.month
                print(f"   Month value: {month_value}")

                # Chamar to_dict
                print(f"   Chamando to_dict()...")
                try:
                    print(f"   Verificando atributos antes de to_dict()...")
                    print(f"   Atributos: {[attr for attr in dir(graph) if not attr.startswith('_')]}")
                    graph_dict = graph.to_dict()
                    print(f"   ✅ to_dict() retornou: {graph_dict}")
                except AttributeError as ae:
                    print(f"   ❌ AttributeError em to_dict(): {ae}")
                    print(f"   Atributos do objeto: {[attr for attr in dir(graph) if not attr.startswith('_')]}")
                    import traceback
                    print(f"   Traceback completo: {traceback.format_exc()}")
                    raise

                graphs_by_month[month_value] = graph_dict
                print(f"   ✅ Gráfico adicionado ao dicionário")

            except Exception as graph_error:
                import traceback
                print(f"❌ Erro ao processar gráfico {graph.id}: {graph_error}")
                print(f"❌ Traceback: {traceback.format_exc()}")

        print(f"\n✅ Total de meses com gráficos: {len(graphs_by_month)}")
        print(f"✅ Meses: {list(graphs_by_month.keys())}")

        result = {
            'success': True,
            'graphs': graphs_by_month,
            'year': year
        }
        print(f"✅ Retornando resultado: {result}")
        print(f"{'='*80}\n")

        return jsonify(result)

    except Exception as e:
        import traceback
        print(f"\n{'='*80}")
        print(f"❌ ERRO CRÍTICO em get_student_graphs")
        print(f"{'='*80}")
        print(f"❌ Erro: {e}")
        print(f"❌ Tipo do erro: {type(e)}")
        print(f"❌ Traceback completo:")
        print(traceback.format_exc())
        print(f"{'='*80}\n")

        return jsonify({
            'error': 'Erro interno do servidor',
            'error_type': type(e).__name__
        }), 500

@graphs_bp.route('/api/student/graphs/upload', methods=['POST'])
@token_required
def upload_student_graph(current_user):
    """Upload de gráfico mensal pelo aluno"""
    try:
        # Verificar se é aluno
        if current_user.type.value != 'student':
            return jsonify({'error': 'Apenas alunos podem fazer upload de gráficos'}), 403
        
        # Verificar dados
        month = request.form.get('month')
        year = request.form.get('year', datetime.now().year, type=int)
        
        if not month or month not in [m.value for m in MonthEnum]:
            return jsonify({'error': 'Mês inválido'}), 400
        
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
        
        # Verificar tamanho do arquivo
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'Arquivo muito grande (máximo 10MB)'}), 400
        
        # Gerar nome único para o arquivo
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        filename = f"graph_{current_user.id}_{month}_{year}_{uuid.uuid4().hex[:8]}.{file_extension}"
        
        # Salvar arquivo
        upload_folder = get_upload_folder()
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # URL relativa para o arquivo
        image_url = f"/api/uploads/graphs/{filename}"
        
        # Verificar se já existe gráfico para este mês/ano
        existing_graph = StudentGraphs.query.filter_by(
            student_id=current_user.id,
            month=MonthEnum(month),
            year=year
        ).first()
        
        if existing_graph:
            # Deletar arquivo antigo
            old_file_path = os.path.join(upload_folder, os.path.basename(existing_graph.image_url))
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
            
            # Atualizar registro
            existing_graph.image_url = image_url
            existing_graph.updated_at = datetime.utcnow()
        else:
            # Criar novo registro
            new_graph = StudentGraphs(
                student_id=current_user.id,
                month=MonthEnum(month),
                year=year,
                image_url=image_url
            )
            db.session.add(new_graph)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Gráfico enviado com sucesso',
            'graph': {
                'month': month,
                'year': year,
                'image_url': image_url
            }
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro no upload do gráfico: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@graphs_bp.route('/api/student/leaks', methods=['GET'])
@token_required
def get_student_leaks(current_user):
    """Buscar análises de leaks do aluno logado"""
    try:
        print(f"\n{'='*80}")
        print(f"🔍 INICIANDO get_student_leaks")
        print(f"{'='*80}")

        year = request.args.get('year', datetime.now().year, type=int)
        print(f"📅 Year recebido: {year}")
        print(f"👤 Student ID: {current_user.id}")
        print(f"👤 Student Type: {current_user.type}")

        # Verificar se StudentLeaks existe
        print(f"🔍 Verificando modelo StudentLeaks...")
        print(f"   Tabela: {StudentLeaks.__tablename__}")

        # Fazer query
        print(f"🔍 Executando query...")
        leaks = StudentLeaks.query.filter_by(
            student_id=current_user.id,
            year=year
        ).all()

        print(f"✅ Leaks encontrados: {len(leaks)}")

        if len(leaks) == 0:
            print(f"⚠️  Nenhum leak encontrado para student_id={current_user.id}, year={year}")
            print(f"   Retornando lista vazia")

        # Organizar por mês
        leaks_by_month = {}
        for idx, leak in enumerate(leaks):
            try:
                print(f"\n📊 Processando leak {idx + 1}/{len(leaks)}")
                print(f"   ID: {leak.id}")
                print(f"   Student ID: {leak.student_id}")
                print(f"   Month: {leak.month}")
                print(f"   Month type: {type(leak.month)}")
                print(f"   Year: {leak.year}")

                # Não tentar acessar os relacionamentos aqui
                print(f"   Pulando acesso aos relacionamentos (será feito no to_dict)")

                # Converter month para value
                month_value = leak.month.value if hasattr(leak.month, 'value') else leak.month
                print(f"   Month value: {month_value}")

                # Chamar to_dict
                print(f"   Chamando to_dict()...")
                leak_dict = leak.to_dict()
                print(f"   ✅ to_dict() retornou: {leak_dict}")

                leaks_by_month[month_value] = leak_dict
                print(f"   ✅ Leak adicionado ao dicionário")

            except Exception as leak_error:
                import traceback
                print(f"❌ Erro ao processar leak {leak.id}: {leak_error}")
                print(f"❌ Traceback: {traceback.format_exc()}")

        print(f"\n✅ Total de meses com leaks: {len(leaks_by_month)}")
        print(f"✅ Meses: {list(leaks_by_month.keys())}")

        result = {
            'success': True,
            'leaks': leaks_by_month,
            'year': year
        }
        print(f"✅ Retornando resultado: {result}")
        print(f"{'='*80}\n")

        return jsonify(result), 200

    except Exception as e:
        import traceback
        print(f"\n{'='*80}")
        print(f"❌ ERRO CRÍTICO em get_student_leaks")
        print(f"{'='*80}")
        print(f"❌ Erro: {e}")
        print(f"❌ Tipo do erro: {type(e)}")
        print(f"❌ Traceback completo:")
        print(traceback.format_exc())
        print(f"{'='*80}\n")

        return jsonify({
            'error': f'Erro interno do servidor: {str(e)}',
            'error_type': type(e).__name__
        }), 500

@graphs_bp.route('/uploads/graphs/<filename>')
def serve_graph_file(filename):
    """Servir arquivos de gráficos"""
    try:
        upload_folder = get_upload_folder()
        return current_app.send_from_directory(upload_folder, filename)
    except Exception as e:
        print(f"❌ Erro ao servir arquivo: {e}")
        return jsonify({'error': 'Arquivo não encontrado'}), 404
