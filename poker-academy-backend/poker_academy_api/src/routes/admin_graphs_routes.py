# src/routes/admin_graphs_routes.py
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from ..models import db, Users, StudentGraphs, StudentLeaks, MonthEnum, Particoes
from ..auth import token_required

admin_graphs_bp = Blueprint('admin_graphs', __name__)

# Configurações de upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_upload_folder():
    """Retorna o diretório de upload para análises de leaks"""
    upload_folder = os.path.join(current_app.config.get('UPLOAD_FOLDER', '/app/uploads'), 'leaks')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

@admin_graphs_bp.route('/api/admin/students-by-partition', methods=['GET'])
@token_required
def get_students_by_partition(current_user):
    """Buscar alunos organizados por partição (apenas admin)"""
    try:
        # Verificar se é admin
        user_type = current_user.type.value if hasattr(current_user.type, 'value') else str(current_user.type)
        print(f"🔍 Verificando tipo de usuário: {user_type} (user_id: {current_user.id})")

        if user_type != 'admin':
            return jsonify({'error': f'Acesso negado. Tipo de usuário: {user_type}'}), 403
        
        # Buscar partições ativas com seus alunos
        partitions = Particoes.query.filter_by(ativa=True).all()
        print(f"📊 Encontradas {len(partitions)} partições ativas")

        result = []
        for partition in partitions:
            students = Users.query.filter_by(
                particao_id=partition.id,
                type='student'
            ).all()
            print(f"📊 Partição {partition.nome}: {len(students)} alunos")

            result.append({
                'id': partition.id,
                'nome': partition.nome,
                'descricao': partition.descricao,
                'students': [student.to_dict() for student in students]
            })

        print(f"📊 Retornando {len(result)} partições com alunos")
        return jsonify({
            'success': True,
            'partitions': result
        })
        
    except Exception as e:
        print(f"❌ Erro ao buscar alunos por partição: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_graphs_bp.route('/api/admin/student/<int:student_id>/graphs', methods=['GET'])
@token_required
def get_student_graphs_admin(current_user, student_id):
    """Buscar gráficos de um aluno específico (apenas admin)"""
    try:
        # Verificar se é admin
        if current_user.type.value != 'admin':
            return jsonify({'error': 'Acesso negado'}), 403
        
        # Verificar se o aluno existe
        student = Users.query.filter_by(id=student_id, type='student').first()
        if not student:
            return jsonify({'error': 'Aluno não encontrado'}), 404
        
        year = request.args.get('year', datetime.now().year, type=int)
        
        graphs = StudentGraphs.query.filter_by(
            student_id=student_id,
            year=year
        ).all()
        
        # Organizar por mês
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
        print(f"❌ Erro ao buscar gráficos do aluno: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_graphs_bp.route('/api/admin/student/<int:student_id>/leaks', methods=['GET'])
@token_required
def get_student_leaks_admin(current_user, student_id):
    """Buscar análises de leaks de um aluno específico (apenas admin)"""
    try:
        # Verificar se é admin
        if current_user.type.value != 'admin':
            return jsonify({'error': 'Acesso negado'}), 403
        
        # Verificar se o aluno existe
        student = Users.query.filter_by(id=student_id, type='student').first()
        if not student:
            return jsonify({'error': 'Aluno não encontrado'}), 404
        
        year = request.args.get('year', datetime.now().year, type=int)
        
        leaks = StudentLeaks.query.filter_by(
            student_id=student_id,
            year=year
        ).all()
        
        # Organizar por mês
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
        print(f"❌ Erro ao buscar leaks do aluno: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_graphs_bp.route('/api/admin/student/<int:student_id>/leaks/upload', methods=['POST'])
@token_required
def upload_student_leak_admin(current_user, student_id):
    """Upload de análise de leak pelo admin"""
    try:
        # Verificar se é admin
        if current_user.type.value != 'admin':
            return jsonify({'error': 'Acesso negado'}), 403
        
        # Verificar se o aluno existe
        student = Users.query.filter_by(id=student_id, type='student').first()
        if not student:
            return jsonify({'error': 'Aluno não encontrado'}), 404
        
        # Verificar dados
        month = request.form.get('month')
        year = request.form.get('year', datetime.now().year, type=int)
        improvements = request.form.get('improvements', '')  # Campo opcional para melhorias

        if not month or month not in [m.value for m in MonthEnum]:
            return jsonify({'error': 'Mês inválido'}), 400

        # Verificar se é apenas melhorias ou upload com arquivo
        improvements_only = request.form.get('improvements_only', 'false').lower() == 'true'
        print(f"🔍 improvements_only: {improvements_only}")
        print(f"🔍 improvements: '{improvements}'")
        print(f"🔍 form data: {dict(request.form)}")

        if not improvements_only:
            # Upload normal com arquivo
            if 'file' not in request.files:
                return jsonify({'error': 'Nenhum arquivo enviado'}), 400

            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

            if not allowed_file(file.filename):
                return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
        else:
            # Apenas melhorias, sem arquivo
            if not improvements.strip():
                return jsonify({'error': 'Melhorias não podem estar vazias'}), 400
        
        # Processar arquivo apenas se não for apenas melhorias
        if not improvements_only:
            # Verificar tamanho do arquivo
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)

            if file_size > MAX_FILE_SIZE:
                return jsonify({'error': 'Arquivo muito grande (máximo 10MB)'}), 400

            # Gerar nome único para o arquivo
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            filename = f"leak_{student_id}_{month}_{year}_{uuid.uuid4().hex[:8]}.{file_extension}"

            # Salvar arquivo
            upload_folder = get_upload_folder()
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            # URL relativa para o arquivo
            image_url = f"/api/uploads/leaks/{filename}"
        else:
            # Apenas melhorias, sem arquivo
            image_url = None
            filename = None
        
        # Verificar se já existe análise para este mês/ano
        existing_leak = StudentLeaks.query.filter_by(
            student_id=student_id,
            month=MonthEnum(month),
            year=year
        ).first()
        
        if existing_leak:
            # Se não for apenas melhorias, deletar arquivo antigo
            if not improvements_only and existing_leak.image_url:
                old_file_path = os.path.join(get_upload_folder(), os.path.basename(existing_leak.image_url))
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Atualizar registro
            if not improvements_only:
                existing_leak.image_url = image_url
            existing_leak.improvements = improvements
            existing_leak.uploaded_by = current_user.id
            existing_leak.updated_at = datetime.utcnow()
        else:
            # Criar novo registro
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
            'message': 'Análise de leak enviada com sucesso',
            'leak': {
                'student_id': student_id,
                'month': month,
                'year': year,
                'image_url': image_url
            }
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro no upload da análise de leak: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_graphs_bp.route('/uploads/leaks/<filename>')
def serve_leak_file(filename):
    """Servir arquivos de análises de leaks"""
    try:
        upload_folder = get_upload_folder()
        return current_app.send_from_directory(upload_folder, filename)
    except Exception as e:
        print(f"❌ Erro ao servir arquivo: {e}")
        return jsonify({'error': 'Arquivo não encontrado'}), 404

@admin_graphs_bp.route('/api/admin/student/<int:student_id>/leaks/improvements', methods=['POST'])
@token_required
def save_student_improvements(current_user, student_id):
    """Salvar apenas melhorias para um aluno (sem upload de arquivo)"""
    try:
        # Verificar se é admin
        if current_user.type.value != 'admin':
            return jsonify({'error': 'Acesso negado'}), 403

        # Verificar se o aluno existe
        student = Users.query.filter_by(id=student_id, type='student').first()
        if not student:
            return jsonify({'error': 'Aluno não encontrado'}), 404

        # Verificar dados
        month = request.form.get('month')
        year = request.form.get('year', datetime.now().year, type=int)
        improvements = request.form.get('improvements', '')

        if not month or month not in [m.value for m in MonthEnum]:
            return jsonify({'error': 'Mês inválido'}), 400

        if not improvements.strip():
            return jsonify({'error': 'Melhorias não podem estar vazias'}), 400

        # Verificar se já existe análise para este mês/ano
        existing_leak = StudentLeaks.query.filter_by(
            student_id=student_id,
            month=MonthEnum(month),
            year=year
        ).first()

        if existing_leak:
            # Atualizar apenas as melhorias
            existing_leak.improvements = improvements
            existing_leak.updated_at = datetime.utcnow()
        else:
            # Criar novo registro apenas com melhorias (sem imagem)
            new_leak = StudentLeaks(
                student_id=student_id,
                month=MonthEnum(month),
                year=year,
                image_url=None,  # NULL para indicar que não há imagem ainda
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
        print(f"❌ Erro ao salvar melhorias: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_graphs_bp.route('/api/admin/test-improvements', methods=['GET'])
@token_required
def test_improvements_endpoint(current_user):
    """Endpoint de teste para verificar se a rota está funcionando"""
    return jsonify({
        'success': True,
        'message': 'Endpoint de melhorias está funcionando',
        'user': current_user.name
    })
