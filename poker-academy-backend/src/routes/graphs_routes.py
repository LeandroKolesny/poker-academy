# src/routes/graphs_routes.py
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
        year = request.args.get('year', datetime.now().year, type=int)
        
        graphs = StudentGraphs.query.filter_by(
            student_id=current_user.id,
            year=year
        ).all()
        
        # Organizar por mês
        graphs_by_month = {}
        for graph in graphs:
            graphs_by_month[graph.month.value] = graph.to_dict()
        
        return jsonify({
            'success': True,
            'graphs': graphs_by_month,
            'year': year
        })
        
    except Exception as e:
        print(f"❌ Erro ao buscar gráficos do aluno: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

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
        year = request.args.get('year', datetime.now().year, type=int)
        
        leaks = StudentLeaks.query.filter_by(
            student_id=current_user.id,
            year=year
        ).all()
        
        # Organizar por mês
        leaks_by_month = {}
        for leak in leaks:
            leaks_by_month[leak.month.value] = leak.to_dict()
        
        return jsonify({
            'success': True,
            'leaks': leaks_by_month,
            'year': year
        })
        
    except Exception as e:
        print(f"❌ Erro ao buscar leaks do aluno: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@graphs_bp.route('/uploads/graphs/<filename>')
def serve_graph_file(filename):
    """Servir arquivos de gráficos"""
    try:
        upload_folder = get_upload_folder()
        return current_app.send_from_directory(upload_folder, filename)
    except Exception as e:
        print(f"❌ Erro ao servir arquivo: {e}")
        return jsonify({'error': 'Arquivo não encontrado'}), 404
