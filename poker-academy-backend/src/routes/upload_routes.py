# src/routes/upload_routes.py
"""
Rotas para upload de arquivos - HIBRIDO.

Em DESENVOLVIMENTO (sem R2 configurado):
1. Frontend pede info de upload ao backend
2. Backend retorna modo 'local'
3. Frontend faz POST para /api/upload/local
4. Backend salva na pasta uploads/

Em PRODUCAO (com R2 configurado):
1. Frontend pede URL pre-assinada
2. Backend retorna modo 'r2' com URL pre-assinada
3. Frontend faz PUT direto no R2
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, send_from_directory
from src.auth import token_required, admin_required
from src.services.r2_service import get_r2_service, LOCAL_UPLOAD_FOLDER

upload_bp = Blueprint("upload_bp", __name__)


@upload_bp.route("/api/upload/status", methods=["GET"])
def upload_status():
    """
    Verifica se o servico de upload esta configurado.
    Util para debug e health check.
    """
    r2 = get_r2_service()

    return jsonify({
        "configured": r2.is_configured(),
        "bucket": os.getenv('R2_BUCKET_NAME', 'nao configurado'),
        "public_url": os.getenv('R2_PUBLIC_URL', 'nao configurado')
    }), 200


@upload_bp.route("/api/upload/presigned-url", methods=["POST"])
@admin_required
def get_presigned_url(current_user):
    """
    Gera uma URL pre-assinada para upload direto ao R2.

    Request JSON:
        {
            "filename": "minha-aula.mp4",
            "folder": "videos"  // opcional, padrao: "videos"
        }

    Response:
        {
            "upload_url": "https://...",      // URL para fazer PUT
            "filename": "videos/20250114_123456_minha-aula.mp4",
            "public_url": "https://pub-xxx.r2.dev/videos/...",
            "content_type": "video/mp4",
            "expires_in": 3600
        }
    """
    r2 = get_r2_service()

    if not r2.is_configured():
        return jsonify(error="Servico de upload nao esta configurado"), 503

    data = request.get_json()

    if not data or 'filename' not in data:
        return jsonify(error="Campo 'filename' e obrigatorio"), 400

    filename = data['filename']
    folder = data.get('folder', 'videos')

    # Validar extensao do arquivo
    if folder == 'videos' and not r2.is_allowed_video(filename):
        return jsonify(
            error=f"Extensao de arquivo nao permitida para videos. Permitidas: mp4, avi, mov, wmv, webm, mkv, flv"
        ), 400

    if folder in ['graphs', 'images'] and not r2.is_allowed_image(filename):
        return jsonify(
            error=f"Extensao de arquivo nao permitida para imagens. Permitidas: jpg, jpeg, png, gif, webp"
        ), 400

    try:
        result = r2.generate_upload_url(filename, folder=folder)
        print(f"[UPLOAD] URL pre-assinada gerada para {current_user.name}: {result['filename']}")
        return jsonify(result), 200

    except Exception as e:
        print(f"[ERROR] Erro ao gerar URL pre-assinada: {e}")
        return jsonify(error=f"Erro ao gerar URL de upload: {str(e)}"), 500


@upload_bp.route("/api/upload/presigned-url/video", methods=["POST"])
@admin_required
def get_video_presigned_url(current_user):
    """
    Atalho para gerar URL pre-assinada especifica para videos.

    Request JSON:
        {
            "filename": "minha-aula.mp4"
        }
    """
    r2 = get_r2_service()

    if not r2.is_configured():
        return jsonify(error="Servico de upload nao esta configurado"), 503

    data = request.get_json()

    if not data or 'filename' not in data:
        return jsonify(error="Campo 'filename' e obrigatorio"), 400

    filename = data['filename']

    if not r2.is_allowed_video(filename):
        return jsonify(
            error="Extensao de video nao permitida. Use: mp4, avi, mov, wmv, webm, mkv, flv"
        ), 400

    try:
        result = r2.generate_upload_url(filename, folder='videos')
        print(f"[VIDEO] URL de video gerada para {current_user.name}: {result['filename']}")
        return jsonify(result), 200

    except Exception as e:
        return jsonify(error=f"Erro ao gerar URL de upload: {str(e)}"), 500


@upload_bp.route("/api/upload/presigned-url/image", methods=["POST"])
@admin_required
def get_image_presigned_url(current_user):
    """
    Atalho para gerar URL pre-assinada especifica para imagens (graficos).

    Request JSON:
        {
            "filename": "grafico-janeiro.png"
        }
    """
    r2 = get_r2_service()

    if not r2.is_configured():
        return jsonify(error="Servico de upload nao esta configurado"), 503

    data = request.get_json()

    if not data or 'filename' not in data:
        return jsonify(error="Campo 'filename' e obrigatorio"), 400

    filename = data['filename']

    if not r2.is_allowed_image(filename):
        return jsonify(
            error="Extensao de imagem nao permitida. Use: jpg, jpeg, png, gif, webp"
        ), 400

    try:
        result = r2.generate_upload_url(filename, folder='graphs')
        print(f"[IMAGE] URL de imagem gerada para {current_user.name}: {result['filename']}")
        return jsonify(result), 200

    except Exception as e:
        return jsonify(error=f"Erro ao gerar URL de upload: {str(e)}"), 500


@upload_bp.route("/api/upload/delete", methods=["DELETE"])
@admin_required
def delete_uploaded_file(current_user):
    """
    Deleta um arquivo do R2.

    Request JSON:
        {
            "filename": "videos/20250114_123456_minha-aula.mp4"
        }
    """
    r2 = get_r2_service()

    if not r2.is_configured():
        return jsonify(error="Servico de upload nao esta configurado"), 503

    data = request.get_json()

    if not data or 'filename' not in data:
        return jsonify(error="Campo 'filename' e obrigatorio"), 400

    filename = data['filename']

    try:
        success = r2.delete_file(filename)

        if success:
            print(f"[DELETE] Arquivo deletado por {current_user.name}: {filename}")
            return jsonify(message="Arquivo deletado com sucesso"), 200
        else:
            return jsonify(error="Falha ao deletar arquivo"), 500

    except Exception as e:
        return jsonify(error=f"Erro ao deletar arquivo: {str(e)}"), 500


@upload_bp.route("/api/upload/list", methods=["GET"])
@admin_required
def list_uploaded_files(current_user):
    """
    Lista arquivos no R2.

    Query params:
        - folder: Pasta para listar (ex: "videos", "graphs")
        - limit: Numero maximo de arquivos (padrao: 50)
    """
    r2 = get_r2_service()

    if not r2.is_configured():
        return jsonify(error="Servico de upload nao esta configurado"), 503

    folder = request.args.get('folder', 'videos')
    limit = request.args.get('limit', 50, type=int)

    try:
        files = r2.list_files(prefix=f"{folder}/", max_keys=limit)
        return jsonify({
            "folder": folder,
            "count": len(files),
            "files": files
        }), 200

    except Exception as e:
        return jsonify(error=f"Erro ao listar arquivos: {str(e)}"), 500


# ============================================
# ROTAS PARA MODO LOCAL (DESENVOLVIMENTO)
# ============================================

@upload_bp.route("/api/upload/local", methods=["POST"])
@admin_required
def upload_local(current_user):
    """
    Upload de arquivo para pasta local (modo desenvolvimento).
    Usado quando R2 nao esta configurado.

    Request: multipart/form-data com campo 'file' e 'filename'
    """
    storage = get_r2_service()

    if storage.is_using_r2():
        return jsonify(error="Use upload direto para R2 em producao"), 400

    if 'file' not in request.files:
        return jsonify(error="Nenhum arquivo enviado"), 400

    file = request.files['file']
    filename = request.form.get('filename')

    if not filename:
        return jsonify(error="Campo 'filename' e obrigatorio"), 400

    if file.filename == '':
        return jsonify(error="Arquivo vazio"), 400

    try:
        # Salvar arquivo localmente
        public_url = storage.save_local_file(file, filename)

        print(f"[SAVE] Upload local por {current_user.name}: {filename}")

        return jsonify({
            "message": "Upload concluido",
            "filename": filename,
            "public_url": public_url,
            "mode": "local"
        }), 200

    except Exception as e:
        print(f"[ERROR] Erro no upload local: {e}")
        return jsonify(error=f"Erro no upload: {str(e)}"), 500


@upload_bp.route("/api/uploads/<path:filename>")
def serve_local_file(filename):
    """
    Serve arquivos da pasta uploads local (modo desenvolvimento).
    Em producao, os arquivos sao servidos diretamente do R2.
    """
    storage = get_r2_service()

    if storage.is_using_r2():
        # Em producao, redirecionar para URL do R2
        public_url = storage.get_public_url(filename)
        return jsonify(error="Arquivo em R2", redirect=public_url), 302

    # Em desenvolvimento, servir arquivo local
    try:
        # Separar diretorio e nome do arquivo
        if '/' in filename:
            directory = os.path.dirname(filename)
            file_only = os.path.basename(filename)
            full_path = os.path.join(LOCAL_UPLOAD_FOLDER, directory)
        else:
            full_path = LOCAL_UPLOAD_FOLDER
            file_only = filename

        return send_from_directory(full_path, file_only)

    except Exception as e:
        print(f"[ERROR] Erro ao servir arquivo: {e}")
        return jsonify(error="Arquivo nao encontrado"), 404
