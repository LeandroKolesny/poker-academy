SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
DELETE FROM particoes WHERE id IN (1, 2);
INSERT INTO particoes (id, nome, descricao, ativa, created_at, updated_at) VALUES 
(1, 'Dojo', 'Partição principal do Dojo', 1, NOW(), NOW()),
(2, 'Coco', 'Partição secundária Coco', 1, NOW(), NOW());
SELECT id, nome, descricao FROM particoes;
