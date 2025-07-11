# src/routes/user_routes.py
import sys
import os

# Adiciona o diretório pai de 'src' (ou seja, 'poker_academy_api') ao sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, current_app
from src.models import db, Users, UserType, Particoes
from src.auth import AuthService, admin_required # Garanta que Users está importado de src.models

user_bp = Blueprint("user_bp", __name__)

# Rota para listar apenas estudantes (para gestão de alunos)
@user_bp.route("/api/users", methods=["GET"])
@admin_required
def get_students(current_user):
    try:
        # Usar SQL direto temporariamente para debug
        from sqlalchemy import text

        # Usar ORM com relacionamento para buscar estudantes
        students = Users.query.filter_by(type=UserType.student).all()
        students_list = [student.to_dict() for student in students]

        return jsonify(students_list), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar estudantes: {e}", exc_info=True)
        return jsonify(error=f"Erro ao buscar dados dos estudantes: {str(e)}"), 500

# Rota para listar TODOS os usuários (incluindo admins) - caso necessário
@user_bp.route("/api/users/all", methods=["GET"])
@admin_required
def get_all_users(current_user):
    try:
        all_users = Users.query.all()
        result = [user.to_dict() for user in all_users]
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar todos os usuários: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar dados dos usuários."), 500

# Rota para criar um novo usuário (apenas admin pode criar outros usuários)
@user_bp.route("/api/users", methods=["POST"])
@admin_required
def create_user(current_user):
    data = request.get_json()
    if not data:
        return jsonify(error="Dados não fornecidos"), 400

    # Frontend envia 'name', 'username', 'email', 'password', 'particao_id'
    required_fields = ["name", "username", "email", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify(error=f"Campo obrigatório ausente ou vazio: {field}"), 400

    # Validação especial para particao_id (deve ser um número válido)
    if "particao_id" not in data or data["particao_id"] is None:
        return jsonify(error="Campo obrigatório ausente: particao_id"), 400

    try:
        particao_id = int(data["particao_id"])
        if particao_id <= 0:
            return jsonify(error="particao_id deve ser um número positivo"), 400
    except (ValueError, TypeError):
        return jsonify(error="particao_id deve ser um número válido"), 400

    # Verificar se a partição existe
    particao = Particoes.query.get(particao_id)
    if not particao:
        return jsonify(error="Partição selecionada não existe."), 400

    if not particao.ativa:
        return jsonify(error="Partição selecionada está inativa."), 400

    # Verificar se email ou username já existem
    if Users.query.filter_by(email=data["email"]).first():
        return jsonify(error="Email já cadastrado."), 409

    if Users.query.filter_by(username=data["username"]).first():
        return jsonify(error="Username já cadastrado."), 409

    try:
        hashed_password = AuthService.hash_password(data["password"])

        # Forçar tipo como 'student' para esta rota (apenas admins são criados no banco)
        new_user = Users(
            name=data["name"],
            username=data["username"],
            email=data["email"],
            password_hash=hashed_password,
            type=UserType.student,  # Sempre criar como student
            particao_id=particao_id  # Chave estrangeira obrigatória
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar usuário: {e}", exc_info=True)
        return jsonify(error=f"Erro ao criar novo usuário: {str(e)}"), 500

# Rota para atualizar um usuário existente
@user_bp.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify(error="Dados não fornecidos"), 400

    user_to_update = Users.query.get(user_id)
    if not user_to_update:
        return jsonify(error="Usuário não encontrado"), 404

    try:
        # Atualiza o nome se fornecido e diferente, e verifica unicidade
        if "name" in data and data["name"] and data["name"] != user_to_update.name:
            if Users.query.filter(Users.id != user_id, Users.name == data["name"]).first():
                return jsonify(error="Nome de usuário (name) já cadastrado."), 409
            user_to_update.name = data["name"]
        
        # Atualiza o email se fornecido e diferente, e verifica unicidade
        if "email" in data and data["email"] and data["email"] != user_to_update.email:
            if Users.query.filter(Users.id != user_id, Users.email == data["email"]).first():
                return jsonify(error="Email já cadastrado."), 409
            user_to_update.email = data["email"]

        # Atualiza a senha se fornecida
        if "password" in data and data["password"]:
            user_to_update.password_hash = AuthService.hash_password(data["password"])
        
        # Atualiza o tipo/role se fornecido
        if "type" in data and data["type"]:
            user_to_update.type = data["type"]

        # Atualiza a partição se fornecida
        if "particao_id" in data and data["particao_id"] is not None:
            try:
                particao_id = int(data["particao_id"])
                if particao_id <= 0:
                    return jsonify(error="particao_id deve ser um número positivo"), 400

                # Verificar se a partição existe e está ativa
                particao = Particoes.query.get(particao_id)
                if not particao:
                    return jsonify(error="Partição selecionada não existe."), 400
                if not particao.ativa:
                    return jsonify(error="Partição selecionada está inativa."), 400
                user_to_update.particao_id = particao_id
            except (ValueError, TypeError):
                return jsonify(error="particao_id deve ser um número válido"), 400
        
        db.session.commit()
        return jsonify(user_to_update.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar usuário {user_id}: {e}", exc_info=True)
        return jsonify(error=f"Erro ao atualizar usuário: {str(e)}"), 500

# Rota para excluir um usuário
@user_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        # Usar conexão raw do MySQL para evitar completamente o ORM
        import pymysql

        # Configurações do banco - usar valores fixos para garantir funcionamento
        connection = pymysql.connect(
            host='db',
            user='root',
            password='Dojo@Sql159357',
            database='poker_academy',
            charset='utf8mb4'
        )

        cursor = connection.cursor()

        try:
            # Verificar se usuário existe
            cursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
            if not cursor.fetchone():
                return jsonify(error="Usuário não encontrado"), 404

            # Desabilitar foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            # Deletar registros relacionados
            cursor.execute(f"DELETE FROM user_progress WHERE user_id = {user_id}")
            cursor.execute(f"DELETE FROM student_graphs WHERE student_id = {user_id}")
            cursor.execute(f"DELETE FROM student_leaks WHERE student_id = {user_id}")
            cursor.execute(f"DELETE FROM student_leaks WHERE uploaded_by = {user_id}")
            cursor.execute(f"DELETE FROM favorites WHERE user_id = {user_id}")
            cursor.execute(f"DELETE FROM playlists WHERE user_id = {user_id}")

            # Deletar o usuário
            cursor.execute(f"DELETE FROM users WHERE id = {user_id}")

            # Reabilitar foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            # Commit das mudanças
            connection.commit()

            return jsonify(message="Usuário excluído com sucesso"), 200

        finally:
            cursor.close()
            connection.close()

    except Exception as e:
        current_app.logger.error(f"Erro ao excluir usuário {user_id}: {e}", exc_info=True)
        return jsonify(error=f"Erro ao excluir usuário: {str(e)}"), 500

# Nova rota para exclusão que não usa SQLAlchemy de forma alguma
@user_bp.route("/api/admin/delete-user/<int:user_id>", methods=["DELETE"])
def admin_delete_user(user_id):
    """Rota especial para exclusão de usuário que bypassa completamente o SQLAlchemy"""
    try:
        import pymysql

        # Conectar diretamente ao MySQL
        connection = pymysql.connect(
            host='db',
            user='root',
            password='Dojo@Sql159357',
            database='poker_academy',
            charset='utf8mb4',
            autocommit=False
        )

        cursor = connection.cursor()

        try:
            # Verificar se usuário existe
            cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return jsonify(error="Usuário não encontrado"), 404

            # Iniciar transação
            cursor.execute("START TRANSACTION")

            # Desabilitar foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            # Deletar registros relacionados em ordem
            tables_to_clean = [
                ("user_progress", "user_id"),
                ("student_graphs", "student_id"),
                ("student_leaks", "student_id"),
                ("student_leaks", "uploaded_by"),
                ("favorites", "user_id"),
                ("playlists", "user_id")
            ]

            for table, column in tables_to_clean:
                cursor.execute(f"DELETE FROM {table} WHERE {column} = %s", (user_id,))
                print(f"Deletados {cursor.rowcount} registros de {table}")

            # Deletar o usuário
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            print(f"Usuário {user_id} deletado")

            # Reabilitar foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            # Commit da transação
            cursor.execute("COMMIT")

            return jsonify(message=f"Usuário {user[1]} ({user[2]}) excluído com sucesso"), 200

        except Exception as e:
            # Rollback em caso de erro
            cursor.execute("ROLLBACK")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            raise e

        finally:
            cursor.close()
            connection.close()

    except Exception as e:
        return jsonify(error=f"Erro ao excluir usuário: {str(e)}"), 500

# Nova rota para exclusão que bypassa completamente o ORM
@user_bp.route("/api/users/<int:user_id>/force-delete", methods=["DELETE"])
def force_delete_user(user_id):
    try:
        # Usar conexão raw do MySQL para evitar completamente o ORM
        import pymysql
        from flask import current_app

        # Configurações do banco
        connection = pymysql.connect(
            host='db',
            user='root',
            password='Dojo@Sql159357',
            database='poker_academy',
            charset='utf8mb4'
        )

        cursor = connection.cursor()

        try:
            # Verificar se usuário existe
            cursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
            if not cursor.fetchone():
                return jsonify(error="Usuário não encontrado"), 404

            # Desabilitar foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            # Deletar registros relacionados
            cursor.execute(f"DELETE FROM user_progress WHERE user_id = {user_id}")
            cursor.execute(f"DELETE FROM student_graphs WHERE student_id = {user_id}")
            cursor.execute(f"DELETE FROM student_leaks WHERE student_id = {user_id}")
            cursor.execute(f"DELETE FROM student_leaks WHERE uploaded_by = {user_id}")
            cursor.execute(f"DELETE FROM favorites WHERE user_id = {user_id}")
            cursor.execute(f"DELETE FROM playlists WHERE user_id = {user_id}")

            # Deletar o usuário
            cursor.execute(f"DELETE FROM users WHERE id = {user_id}")

            # Reabilitar foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            # Commit das mudanças
            connection.commit()

            return jsonify(message="Usuário excluído com sucesso"), 200

        finally:
            cursor.close()
            connection.close()

    except Exception as e:
        current_app.logger.error(f"Erro ao excluir usuário {user_id}: {e}", exc_info=True)
        return jsonify(error=f"Erro ao excluir usuário: {str(e)}"), 500

