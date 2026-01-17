# src/routes/database_routes.py
# Database mensal routes - Upload e download de arquivos .zip com dados de mãos jogadas
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from ..models import db, Users, StudentDatabase, MonthEnum
from ..auth import token_required

database_bp = Blueprint('database', __name__)

# Configurações de upload
ALLOWED_EXTENSIONS = {'zip'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_upload_folder():
    """Retorna o diretório de upload para databases"""
    upload_folder = os.path.join(current_app.config.get('UPLOAD_FOLDER', '/app/uploads'), 'databases')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

@database_bp.route('/api/student/database', methods=['GET'])
@token_required
def get_student_database(current_user):
    """Buscar databases do aluno logado ou de todos os alunos (se admin)"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        
        if current_user.type.value == 'admin':
            # Admin vê todos os databases
            databases = StudentDatabase.query.filter_by(year=year).all()
        else:
            # Aluno vê apenas seus databases
            databases = StudentDatabase.query.filter_by(
                student_id=current_user.id,
                year=year
            ).all()
        
        result = [db_record.to_dict() for db_record in databases]
        
        # Se for admin, adicionar nome do aluno
        if current_user.type.value == 'admin':
            for item in result:
                student = Users.query.get(item['student_id'])
                item['student_name'] = student.name if student else 'Desconhecido'
        
        return jsonify({'data': result}), 200
    
    except Exception as e:
        print(f"❌ Erro ao buscar databases: {e}")
        return jsonify({'error': str(e)}), 500

@database_bp.route('/api/student/database/upload', methods=['POST'])
@token_required
def upload_student_database(current_user):
    """Upload de database mensal (arquivo .zip) pelo aluno"""
    try:
        # Verificar se é aluno
        if current_user.type.value != 'student':
            return jsonify({'error': 'Apenas alunos podem fazer upload de database'}), 403
        
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
            return jsonify({'error': 'Apenas arquivos .zip são permitidos'}), 400
        
        # Verificar tamanho do arquivo
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'Arquivo muito grande (máximo 500MB)'}), 400
        
        # Gerar nome único para o arquivo
        filename = f"db_{current_user.id}_{month}_{year}_{uuid.uuid4().hex[:8]}.zip"
        
        # Salvar arquivo
        upload_folder = get_upload_folder()
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # URL relativa para o arquivo
        file_url = f"/api/uploads/databases/{filename}"
        
        # Verificar se já existe database para este mês/ano
        existing_db = StudentDatabase.query.filter_by(
            student_id=current_user.id,
            month=MonthEnum(month),
            year=year
        ).first()
        
        if existing_db:
            # Deletar arquivo antigo
            old_file_path = os.path.join(upload_folder, os.path.basename(existing_db.file_url))
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

            # Atualizar registro
            existing_db.file_url = file_url
            existing_db.file_size = file_size
            existing_db.status = 'ativo'  # Reativar se estava deletado
            existing_db.updated_at = datetime.utcnow()
        else:
            # Criar novo registro
            new_db = StudentDatabase(
                student_id=current_user.id,
                month=MonthEnum(month),
                year=year,
                file_url=file_url,
                file_size=file_size,
                status='ativo'
            )
            db.session.add(new_db)
        
        db.session.commit()
        
        return jsonify({
            'data': {
                'message': 'Database enviado com sucesso',
                'file_url': file_url,
                'file_size': file_size
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao fazer upload de database: {e}")
        return jsonify({'error': str(e)}), 500

@database_bp.route('/api/student/database/download/<filename>', methods=['GET'])
@token_required
def download_database(current_user, filename):
    """Download de arquivo de database"""
    try:
        # Validar nome do arquivo
        filename = secure_filename(filename)

        # Buscar registro no banco
        db_record = StudentDatabase.query.filter(
            StudentDatabase.file_url.like(f'%{filename}')
        ).first()

        if not db_record:
            print(f"❌ Arquivo não encontrado no banco: {filename}")
            return jsonify({'error': 'Arquivo não encontrado'}), 404

        # Verificar permissões
        if current_user.type.value == 'student' and db_record.student_id != current_user.id:
            return jsonify({'error': 'Acesso negado'}), 403

        # Servir arquivo
        upload_folder = get_upload_folder()
        file_path = os.path.join(upload_folder, filename)

        if not os.path.exists(file_path):
            print(f"❌ Arquivo não existe no disco: {file_path}")
            return jsonify({'error': 'Arquivo não encontrado no servidor'}), 404

        print(f"✅ Servindo arquivo: {file_path}")
        return send_from_directory(upload_folder, filename, as_attachment=True)

    except Exception as e:
        print(f"❌ Erro ao fazer download de database: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Arquivo não encontrado'}), 404

@database_bp.route('/api/uploads/databases/<filename>')
def serve_database_file(filename):
    """Servir arquivos de database"""
    try:
        upload_folder = get_upload_folder()
        return send_from_directory(upload_folder, filename)
    except Exception as e:
        print(f"❌ Erro ao servir arquivo: {e}")
        return jsonify({'error': 'Arquivo não encontrado'}), 404

