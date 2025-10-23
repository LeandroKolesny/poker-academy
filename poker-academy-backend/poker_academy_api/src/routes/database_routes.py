# src/routes/database_routes.py
# Database mensal routes - Upload e download de arquivos .zip com dados de mãos jogadas
from flask import Blueprint, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from ..models import db, Users, StudentDatabase, MonthEnum, Particoes
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

def cleanup_expired_databases():
    """Verifica e marca como deletado arquivos que expiraram (mais de 5 minutos)"""
    try:
        from datetime import timedelta

        # Buscar todos os arquivos de database com status 'ativo'
        all_databases = StudentDatabase.query.filter_by(status='ativo').all()
        now = datetime.utcnow()  # Usar UTC para consistência
        expiration_time = timedelta(minutes=5)

        print(f"🔍 Verificando {len(all_databases)} arquivo(s) para limpeza...")
        deleted_count = 0
        for db_record in all_databases:
            # Calcular tempo desde criação
            time_since_creation = now - db_record.created_at
            print(f"   - {db_record.file_url}: {time_since_creation.total_seconds():.0f}s desde criação")

            # Se passou 5 minutos, marcar como deletado
            if time_since_creation > expiration_time:
                try:
                    # Deletar arquivo do disco
                    upload_folder = get_upload_folder()
                    filename = db_record.file_url.split('/')[-1]
                    file_path = os.path.join(upload_folder, filename)

                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"🗑️ Arquivo deletado do disco: {filename}")

                    # Marcar como deletado no banco
                    db_record.status = 'deletado'
                    db_record.updated_at = datetime.utcnow()
                    deleted_count += 1
                    print(f"✅ Arquivo marcado como deletado: {filename}")

                except Exception as e:
                    print(f"❌ Erro ao processar arquivo {db_record.file_url}: {e}")

        if deleted_count > 0:
            db.session.commit()
            print(f"✅ {deleted_count} arquivo(s) expirado(s) marcado(s) como deletado(s)")
        else:
            print(f"ℹ️ Nenhum arquivo expirado encontrado")

    except Exception as e:
        print(f"❌ Erro na limpeza de arquivos expirados: {e}")

@database_bp.route('/api/student/database', methods=['GET'])
@token_required
def get_student_database(current_user):
    """Buscar databases do aluno logado ou de todos os alunos (se admin)"""
    try:
        # Limpar arquivos expirados (mais de 5 minutos)
        cleanup_expired_databases()

        year = request.args.get('year', datetime.now().year, type=int)
        particao_id = request.args.get('particao_id', None, type=int)

        if current_user.type.value == 'admin':
            # Admin vê todos os databases
            if particao_id:
                # Filtrar por partição
                students_in_partition = Users.query.filter_by(particao_id=particao_id).all()
                student_ids = [s.id for s in students_in_partition]
                databases = StudentDatabase.query.filter(
                    StudentDatabase.year == year,
                    StudentDatabase.student_id.in_(student_ids)
                ).all()
            else:
                # Sem filtro de partição, retorna todos
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
            existing_db.updated_at = datetime.utcnow()
        else:
            # Criar novo registro
            new_db = StudentDatabase(
                student_id=current_user.id,
                month=MonthEnum(month),
                year=year,
                file_url=file_url,
                file_size=file_size
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
        print(f"🔍 Download request: filename={filename}, user={current_user.id}")

        # Buscar registro no banco
        db_record = StudentDatabase.query.filter(
            StudentDatabase.file_url.like(f'%{filename}')
        ).first()

        print(f"🔍 DB record found: {db_record is not None}")
        if not db_record:
            print(f"❌ Arquivo não encontrado no banco para: {filename}")
            return jsonify({'error': 'Arquivo não encontrado'}), 404

        # Verificar permissões
        if current_user.type.value == 'student' and db_record.student_id != current_user.id:
            print(f"❌ Acesso negado: student_id={db_record.student_id}, current_user={current_user.id}")
            return jsonify({'error': 'Acesso negado'}), 403

        # Servir arquivo
        upload_folder = get_upload_folder()
        file_path = os.path.join(upload_folder, filename)

        print(f"🔍 File path: {file_path}")
        print(f"🔍 File exists: {os.path.exists(file_path)}")

        if not os.path.exists(file_path):
            print(f"❌ Arquivo não existe no servidor: {file_path}")
            return jsonify({'error': 'Arquivo não encontrado no servidor'}), 404

        print(f"✅ Servindo arquivo: {filename}")
        return send_file(file_path, as_attachment=True, download_name=filename)

    except Exception as e:
        print(f"❌ Erro ao fazer download de database: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Arquivo não encontrado'}), 404

@database_bp.route('/api/uploads/databases/<filename>')
def serve_database_file(filename):
    """Servir arquivos de database"""
    try:
        filename = secure_filename(filename)
        upload_folder = get_upload_folder()
        file_path = os.path.join(upload_folder, filename)

        if not os.path.exists(file_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404

        return send_file(file_path, as_attachment=False)
    except Exception as e:
        print(f"❌ Erro ao servir arquivo: {e}")
        return jsonify({'error': 'Arquivo não encontrado'}), 404

@database_bp.route('/api/particoes', methods=['GET'])
@token_required
def get_particoes(current_user):
    """Listar todas as partições (apenas para admin)"""
    try:
        if current_user.type.value != 'admin':
            return jsonify({'error': 'Apenas admins podem acessar partições'}), 403

        particoes = Particoes.query.filter_by(ativa=True).all()
        result = [
            {
                'id': p.id,
                'nome': p.nome,
                'descricao': p.descricao
            }
            for p in particoes
        ]

        return jsonify({'data': result}), 200

    except Exception as e:
        print(f"❌ Erro ao buscar partições: {e}")
        return jsonify({'error': str(e)}), 500

