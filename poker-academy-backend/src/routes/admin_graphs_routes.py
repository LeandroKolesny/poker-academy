# src/routes/admin_graphs_routes.py
# Rotas para gerenciamento de graficos e leaks dos alunos
# HIBRIDO: Usa R2 em producao, pasta local em desenvolvimento
from flask import Blueprint, request, jsonify, current_app, send_from_directory, redirect
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from ..models import db, Users, StudentGraphs, StudentLeaks, MonthEnum, Particoes
from ..auth import token_required
from ..services.r2_service import get_storage_service, LOCAL_UPLOAD_FOLDER

admin_graphs_bp = Blueprint('admin_graphs', __name__)

# Configuracoes de upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_graphs_upload_folder():
    """Retorna o diretorio de upload para graficos (modo local)"""
    upload_folder = os.path.join(current_app.config.get('UPLOAD_FOLDER', '/app/uploads'), 'graphs')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

def get_leaks_upload_folder():
    """Retorna o diretorio de upload para leaks (modo local)"""
    upload_folder = os.path.join(current_app.config.get('UPLOAD_FOLDER', '/app/uploads'), 'leaks')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

@admin_graphs_bp.route('/api/admin/students-by-partition', methods=['GET'])
@token_required
def get_students_by_partition(current_user):
    """Buscar alunos organizados por particao (apenas admin)"""
    try:
        # Verificar se e admin
        user_type = current_user.type.value if hasattr(current_user.type, 'value') else str(current_user.type)

        if user_type != 'admin':
            return jsonify({'error': f'Acesso negado. Tipo de usuario: {user_type}'}), 403

        # Obter parametro de filtro de particao (opcional)
        particao_id = request.args.get('particao_id', type=int)

        # Buscar particoes ativas com seus alunos
        if particao_id:
            partitions = Particoes.query.filter_by(id=particao_id, ativa=True).all()
        else:
            partitions = Particoes.query.filter_by(ativa=True).all()

        result = []
        for partition in partitions:
            students = Users.query.filter_by(
                particao_id=partition.id,
                type='student'
            ).all()

            result.append({
                'id': partition.id,
                'nome': partition.nome,
                'descricao': partition.descricao,
                'students': [student.to_dict() for student in students]
            })

        return jsonify({
            'success': True,
            'partitions': result
        })

    except Exception as e:
        print(f"[ERROR] Erro ao buscar alunos por particao: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ============================================
# ROTAS DE GRAFICOS (GRAPHS)
# ============================================

@admin_graphs_bp.route('/api/admin/student/<int:student_id>/graphs', methods=['GET'])
@token_required
def get_student_graphs_admin(current_user, student_id):
    """Buscar graficos de um aluno especifico (apenas admin)"""
    try:
        if current_user.type.value != 'admin':
            return jsonify({'error': 'Acesso negado'}), 403

        student = Users.query.filter_by(id=student_id, type='student').first()
        if not student:
            return jsonify({'error': 'Aluno nao encontrado'}), 404

        year = request.args.get('year', datetime.now().year, type=int)

        graphs = StudentGraphs.query.filter_by(
            student_id=student_id,
            year=year
        ).all()

        graphs_by_month = {}
        for graph in graphs:
            graphs_by_month[graph.month.value] = graph.to_dict()

        return jsonify({
            'success': True,
            'student': student.to_dict(),
            'graphs': graphs_by_month,
            'year': year
        })

    except Exception as e:
        print(f"[ERROR] Erro ao buscar graficos do aluno: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_graphs_bp.route('/api/admin/student/<int:student_id>/graphs/upload', methods=['POST', 'OPTIONS'])
@token_required
def upload_student_graph_admin(current_user, student_id):
    """Upload de grafico mensal pelo admin - USA R2 ou LOCAL"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        if current_user.type.value != 'admin':
            return jsonify({'error': 'Acesso negado'}), 403

        student = Users.query.filter_by(id=student_id, type='student').first()
        if not student:
            return jsonify({'error': 'Aluno nao encontrado'}), 404

        month = request.form.get('month')
        year = request.form.get('year', datetime.now().year, type=int)

        if not month or month not in [m.value for m in MonthEnum]:
            return jsonify({'error': 'Mes invalido'}), 400

        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de arquivo nao permitido'}), 400

        # Verificar tamanho
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'Arquivo muito grande (maximo 10MB)'}), 400

        # Obter servico de storage (R2 ou local automaticamente)
        storage = get_storage_service()

        # Gerar nome unico
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        original_filename = f"graph_{student_id}_{month}_{year}.{file_extension}"

        # Fazer upload (R2 ou local)
        result = storage.upload_file_directly(file, 'graphs', original_filename)
        image_url = result['public_url']

        print(f"[GRAPHS] Upload via {result['mode']}: {image_url}")

        # Verificar se ja existe grafico para este mes/ano
        existing_graph = StudentGraphs.query.filter_by(
            student_id=student_id,
            month=MonthEnum(month),
            year=year
        ).first()

        if existing_graph:
            # Deletar arquivo antigo
            if existing_graph.image_url:
                old_key = f"graphs/{existing_graph.image_url.split('/')[-1]}"
                storage.delete_file(old_key)

            existing_graph.image_url = image_url
            existing_graph.updated_at = datetime.utcnow()
        else:
            new_graph = StudentGraphs(
                student_id=student_id,
                month=MonthEnum(month),
                year=year,
                image_url=image_url
            )
            db.session.add(new_graph)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Grafico enviado com sucesso',
            'graph': {
                'student_id': student_id,
                'month': month,
                'year': year,
                'image_url': image_url,
                'storage_mode': result['mode']
            }
        })

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Erro no upload do grafico: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ============================================
# ROTAS DE LEAKS
# ============================================

@admin_graphs_bp.route('/api/admin/student/<int:student_id>/leaks', methods=['GET'])
@token_required
def get_student_leaks_admin(current_user, student_id):
    """Buscar analises de leaks de um aluno especifico (apenas admin)"""
    try:
        if current_user.type.value != 'admin':
            return jsonify({'error': 'Acesso negado'}), 403

        student = Users.query.filter_by(id=student_id, type='student').first()
        if not student:
            return jsonify({'error': 'Aluno nao encontrado'}), 404

        year = request.args.get('year', datetime.now().year, type=int)

        leaks = StudentLeaks.query.filter_by(
            student_id=student_id,
            year=year
        ).all()

        leaks_by_month = {}
        for leak in leaks:
            leaks_by_month[leak.month.value] = leak.to_dict()

        return jsonify({
            'success': True,
            'student': student.to_dict(),
            'leaks': leaks_by_month,
            'year': year
        })

    except Exception as e:
        print(f"[ERROR] Erro ao buscar leaks do aluno: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_graphs_bp.route('/api/admin/student/<int:student_id>/leaks/upload', methods=['POST', 'OPTIONS'])
@token_required
def upload_student_leak_admin(current_user, student_id):
    """Upload de analise de leak pelo admin - USA R2 ou LOCAL"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        if current_user.type.value != 'admin':
            return jsonify({'error': 'Acesso negado'}), 403

        student = Users.query.filter_by(id=student_id, type='student').first()
        if not student:
            return jsonify({'error': 'Aluno nao encontrado'}), 404

        month = request.form.get('month')
        year = request.form.get('year', datetime.now().year, type=int)
        improvements = request.form.get('improvements', '')

        if not month or month not in [m.value for m in MonthEnum]:
            return jsonify({'error': 'Mes invalido'}), 400

        # Verificar se e apenas melhorias ou upload com arquivo
        improvements_only = request.form.get('improvements_only', 'false').lower() == 'true'

        storage = get_storage_service()
        image_url = None

        if improvements_only:
            if not improvements.strip():
                return jsonify({'error': 'Melhorias nao podem estar vazias'}), 400
        else:
            if 'file' not in request.files:
                return jsonify({'error': 'Nenhum arquivo enviado'}), 400

            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

            if not allowed_file(file.filename):
                return jsonify({'error': 'Tipo de arquivo nao permitido'}), 400

            # Verificar tamanho
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)

            if file_size > MAX_FILE_SIZE:
                return jsonify({'error': 'Arquivo muito grande (maximo 10MB)'}), 400

            # Gerar nome unico
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            original_filename = f"leak_{student_id}_{month}_{year}.{file_extension}"

            # Fazer upload (R2 ou local)
            result = storage.upload_file_directly(file, 'leaks', original_filename)
            image_url = result['public_url']

            print(f"[LEAKS] Upload via {result['mode']}: {image_url}")

        # Verificar se ja existe analise para este mes/ano
        existing_leak = StudentLeaks.query.filter_by(
            student_id=student_id,
            month=MonthEnum(month),
            year=year
        ).first()

        if existing_leak:
            # Se ha arquivo novo, deletar arquivo antigo
            if image_url and existing_leak.image_url:
                old_key = f"leaks/{existing_leak.image_url.split('/')[-1]}"
                storage.delete_file(old_key)

            if image_url:
                existing_leak.image_url = image_url
            existing_leak.improvements = improvements
            existing_leak.uploaded_by = current_user.id
            existing_leak.updated_at = datetime.utcnow()
        else:
            new_leak = StudentLeaks(
                student_id=student_id,
                month=MonthEnum(month),
                year=year,
                image_url=image_url,
                improvements=improvements,
                uploaded_by=current_user.id
            )
            db.session.add(new_leak)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Analise de leak enviada com sucesso',
            'leak': {
                'student_id': student_id,
                'month': month,
                'year': year,
                'image_url': image_url
            }
        })

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Erro no upload da analise de leak: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_graphs_bp.route('/api/admin/student/<int:student_id>/leaks/improvements', methods=['POST'])
@token_required
def save_student_improvements(current_user, student_id):
    """Salvar apenas melhorias para um aluno (sem upload de arquivo)"""
    try:
        if current_user.type.value != 'admin':
            return jsonify({'error': 'Acesso negado'}), 403

        student = Users.query.filter_by(id=student_id, type='student').first()
        if not student:
            return jsonify({'error': 'Aluno nao encontrado'}), 404

        month = request.form.get('month')
        year = request.form.get('year', datetime.now().year, type=int)
        improvements = request.form.get('improvements', '')

        if not month or month not in [m.value for m in MonthEnum]:
            return jsonify({'error': 'Mes invalido'}), 400

        if not improvements.strip():
            return jsonify({'error': 'Melhorias nao podem estar vazias'}), 400

        existing_leak = StudentLeaks.query.filter_by(
            student_id=student_id,
            month=MonthEnum(month),
            year=year
        ).first()

        if existing_leak:
            existing_leak.improvements = improvements
            existing_leak.updated_at = datetime.utcnow()
        else:
            new_leak = StudentLeaks(
                student_id=student_id,
                month=MonthEnum(month),
                year=year,
                image_url=None,
                improvements=improvements,
                uploaded_by=current_user.id
            )
            db.session.add(new_leak)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Melhorias salvas com sucesso',
            'improvements': improvements
        })

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Erro ao salvar melhorias: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ============================================
# ROTAS PARA SERVIR ARQUIVOS
# ============================================

@admin_graphs_bp.route('/api/uploads/graphs/<filename>')
def serve_graph_file(filename):
    """Servir arquivos de graficos"""
    try:
        storage = get_storage_service()

        if storage.is_using_r2():
            public_url = storage.get_public_url(f"graphs/{filename}")
            return redirect(public_url)
        else:
            upload_folder = get_graphs_upload_folder()
            return send_from_directory(upload_folder, filename)
    except Exception as e:
        print(f"[ERROR] Erro ao servir arquivo: {e}")
        return jsonify({'error': 'Arquivo nao encontrado'}), 404

@admin_graphs_bp.route('/api/uploads/leaks/<filename>')
def serve_leak_file(filename):
    """Servir arquivos de analises de leaks"""
    try:
        storage = get_storage_service()

        if storage.is_using_r2():
            public_url = storage.get_public_url(f"leaks/{filename}")
            return redirect(public_url)
        else:
            upload_folder = get_leaks_upload_folder()
            return send_from_directory(upload_folder, filename)
    except Exception as e:
        print(f"[ERROR] Erro ao servir arquivo: {e}")
        return jsonify({'error': 'Arquivo nao encontrado'}), 404

@admin_graphs_bp.route('/uploads/leaks/<filename>')
def serve_leak_file_legacy(filename):
    """Rota legada para compatibilidade"""
    return serve_leak_file(filename)

@admin_graphs_bp.route('/api/admin/test-improvements', methods=['GET'])
@token_required
def test_improvements_endpoint(current_user):
    """Endpoint de teste"""
    storage = get_storage_service()
    return jsonify({
        'success': True,
        'message': 'Endpoint funcionando',
        'storage_mode': 'r2' if storage.is_using_r2() else 'local',
        'user': current_user.name
    })
