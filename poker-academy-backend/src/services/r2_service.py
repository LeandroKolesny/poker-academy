# src/services/r2_service.py
"""
Servico de storage para videos - HIBRIDO.
- Em PRODUCAO: usa Cloudflare R2 (quando R2_ACCOUNT_ID esta configurado)
- Em DESENVOLVIMENTO: usa pasta local (quando R2 nao esta configurado)

O sistema detecta automaticamente baseado nas variaveis de ambiente.
"""

import os
import shutil
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app, url_for

# Extensoes permitidas
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'webm', 'mkv', 'flv'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

# Pasta para uploads locais (desenvolvimento)
LOCAL_UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'uploads'
)


class StorageService:
    """
    Servico de storage hibrido - usa R2 em producao e pasta local em desenvolvimento.

    Uso:
        storage = StorageService()

        # Verificar modo
        if storage.is_using_r2():
            print("Usando R2")
        else:
            print("Usando storage local")

        # Upload (funciona igual nos dois modos)
        result = storage.prepare_upload("video.mp4", folder="videos")
    """

    def __init__(self):
        """Inicializa o servico de storage."""
        self.account_id = os.getenv('R2_ACCOUNT_ID')
        self.access_key = os.getenv('R2_ACCESS_KEY_ID')
        self.secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
        self.bucket_name = os.getenv('R2_BUCKET_NAME', 'cardroomgrinders-videos')
        self.public_url = os.getenv('R2_PUBLIC_URL', '')

        # Verificar se R2 esta configurado
        self._use_r2 = all([self.account_id, self.access_key, self.secret_key])

        if self._use_r2:
            # Importar boto3 apenas se for usar R2
            try:
                import boto3
                from botocore.config import Config

                self.endpoint_url = os.getenv(
                    'R2_ENDPOINT_URL',
                    f'https://{self.account_id}.r2.cloudflarestorage.com'
                )

                self.s3_client = boto3.client(
                    's3',
                    endpoint_url=self.endpoint_url,
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key,
                    config=Config(
                        signature_version='s3v4',
                        s3={'addressing_style': 'path'}
                    )
                )
                print(f"[Storage] R2 (Cloudflare) - Bucket: {self.bucket_name}")

            except ImportError:
                print("[WARN] boto3 nao instalado - usando storage local")
                self._use_r2 = False
                self.s3_client = None
        else:
            self.s3_client = None
            print(f"[Storage] LOCAL - Pasta: {LOCAL_UPLOAD_FOLDER}")

        # Criar pasta local se necessario
        if not self._use_r2:
            os.makedirs(os.path.join(LOCAL_UPLOAD_FOLDER, 'videos'), exist_ok=True)
            os.makedirs(os.path.join(LOCAL_UPLOAD_FOLDER, 'graphs'), exist_ok=True)

    def is_using_r2(self) -> bool:
        """Retorna True se esta usando R2, False se local."""
        return self._use_r2

    def is_configured(self) -> bool:
        """Retorna True se o servico esta pronto para uso."""
        return True  # Sempre configurado (local ou R2)

    def _generate_unique_filename(self, original_filename: str) -> str:
        """Gera nome unico com timestamp."""
        safe_filename = secure_filename(original_filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{safe_filename}"

    def _get_content_type(self, filename: str) -> str:
        """Retorna content-type baseado na extensao."""
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        content_types = {
            'mp4': 'video/mp4',
            'avi': 'video/x-msvideo',
            'mov': 'video/quicktime',
            'wmv': 'video/x-ms-wmv',
            'webm': 'video/webm',
            'mkv': 'video/x-matroska',
            'flv': 'video/x-flv',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp',
        }
        return content_types.get(ext, 'application/octet-stream')

    def is_allowed_video(self, filename: str) -> bool:
        """Verifica se e um video permitido."""
        if '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[-1].lower()
        return ext in ALLOWED_VIDEO_EXTENSIONS

    def is_allowed_image(self, filename: str) -> bool:
        """Verifica se e uma imagem permitida."""
        if '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[-1].lower()
        return ext in ALLOWED_IMAGE_EXTENSIONS

    def generate_upload_url(self, original_filename: str, folder: str = "videos", expires_in: int = 3600) -> dict:
        """
        Prepara upload - retorna URL pre-assinada (R2) ou info para upload local.

        Retorna dict com:
        - upload_url: URL para PUT (R2) ou endpoint local
        - filename: Nome do arquivo gerado
        - public_url: URL publica apos upload
        - mode: 'r2' ou 'local'
        """
        unique_filename = self._generate_unique_filename(original_filename)
        key = f"{folder}/{unique_filename}" if folder else unique_filename
        content_type = self._get_content_type(original_filename)

        if self._use_r2:
            # Modo R2 - gerar URL pre-assinada
            from botocore.exceptions import ClientError

            try:
                upload_url = self.s3_client.generate_presigned_url(
                    'put_object',
                    Params={
                        'Bucket': self.bucket_name,
                        'Key': key,
                        'ContentType': content_type
                    },
                    ExpiresIn=expires_in
                )

                public_url = f"{self.public_url}/{key}" if self.public_url else None

                return {
                    'upload_url': upload_url,
                    'filename': key,
                    'public_url': public_url,
                    'content_type': content_type,
                    'expires_in': expires_in,
                    'mode': 'r2'
                }

            except ClientError as e:
                print(f"[ERROR] Erro ao gerar URL R2: {e}")
                raise

        else:
            # Modo LOCAL - retornar endpoint do backend
            # O frontend vai fazer POST para /api/upload/local
            return {
                'upload_url': '/api/upload/local',
                'filename': key,
                'public_url': f'/api/uploads/{key}',
                'content_type': content_type,
                'expires_in': None,
                'mode': 'local'
            }

    def save_local_file(self, file, filename: str) -> str:
        """
        Salva arquivo localmente (usado em desenvolvimento).

        Args:
            file: Objeto file do Flask (request.files['video'])
            filename: Nome do arquivo (ex: 'videos/20250114_video.mp4')

        Returns:
            URL publica do arquivo
        """
        if self._use_r2:
            raise RuntimeError("Use upload direto para R2, nao save_local_file")

        filepath = os.path.join(LOCAL_UPLOAD_FOLDER, filename)

        # Criar diretorio se nao existir
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Salvar arquivo
        file.save(filepath)
        print(f"[SAVE] Arquivo salvo localmente: {filepath}")

        return f'/api/uploads/{filename}'

    def get_local_filepath(self, filename: str) -> str:
        """Retorna caminho completo do arquivo local."""
        return os.path.join(LOCAL_UPLOAD_FOLDER, filename)

    def get_public_url(self, filename: str) -> str:
        """Retorna URL publica do arquivo."""
        if self._use_r2:
            return f"{self.public_url}/{filename}"
        else:
            return f'/api/uploads/{filename}'

    def delete_file(self, filename: str) -> bool:
        """Deleta arquivo (R2 ou local)."""
        if self._use_r2:
            from botocore.exceptions import ClientError
            try:
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=filename)
                print(f"[DELETE] Arquivo deletado do R2: {filename}")
                return True
            except ClientError as e:
                print(f"[ERROR] Erro ao deletar do R2: {e}")
                return False
        else:
            filepath = os.path.join(LOCAL_UPLOAD_FOLDER, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"[DELETE] Arquivo deletado localmente: {filepath}")
                return True
            return False

    def file_exists(self, filename: str) -> bool:
        """Verifica se arquivo existe."""
        if self._use_r2:
            from botocore.exceptions import ClientError
            try:
                self.s3_client.head_object(Bucket=self.bucket_name, Key=filename)
                return True
            except ClientError:
                return False
        else:
            filepath = os.path.join(LOCAL_UPLOAD_FOLDER, filename)
            return os.path.exists(filepath)

    def list_files(self, prefix: str = "", max_keys: int = 100) -> list:
        """Lista arquivos."""
        if self._use_r2:
            from botocore.exceptions import ClientError
            try:
                response = self.s3_client.list_objects_v2(
                    Bucket=self.bucket_name,
                    Prefix=prefix,
                    MaxKeys=max_keys
                )
                files = []
                for obj in response.get('Contents', []):
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat(),
                        'public_url': f"{self.public_url}/{obj['Key']}"
                    })
                return files
            except ClientError as e:
                print(f"[ERROR] Erro ao listar R2: {e}")
                return []
        else:
            # Listar arquivos locais
            folder_path = os.path.join(LOCAL_UPLOAD_FOLDER, prefix)
            files = []
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path):
                    filepath = os.path.join(folder_path, filename)
                    if os.path.isfile(filepath):
                        stat = os.stat(filepath)
                        files.append({
                            'key': f"{prefix}{filename}",
                            'size': stat.st_size,
                            'last_modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            'public_url': f'/api/uploads/{prefix}{filename}'
                        })
            return files[:max_keys]


# Singleton
_storage_service_instance = None


def get_r2_service() -> StorageService:
    """Retorna instancia do StorageService (nome mantido para compatibilidade)."""
    global _storage_service_instance
    if _storage_service_instance is None:
        _storage_service_instance = StorageService()
    return _storage_service_instance


# Alias para clareza
def get_storage_service() -> StorageService:
    """Alias para get_r2_service."""
    return get_r2_service()
