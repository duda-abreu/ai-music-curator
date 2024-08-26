-- Inserir usuários (verifica se o ID não existe antes de inserir)
INSERT INTO Usuarios (id, nome)
SELECT 1, 'João'
WHERE NOT EXISTS (SELECT 1 FROM Usuarios WHERE id = 1);

INSERT INTO Usuarios (id, nome)
SELECT 2, 'Maria'
WHERE NOT EXISTS (SELECT 1 FROM Usuarios WHERE id = 2);

-- Inserir músicas
INSERT INTO Musicas (id, titulo, artista, album, genero)
SELECT 1, 'Song 1', 'Artist 1', 'Album 1', '{pop, rock}'
WHERE NOT EXISTS (SELECT 1 FROM Musicas WHERE id = 1);

INSERT INTO Musicas (id, titulo, artista, album, genero)
SELECT 2, 'Song 2', 'Artist 2', 'Album 2', '{pop}'
WHERE NOT EXISTS (SELECT 1 FROM Musicas WHERE id = 2);

INSERT INTO Musicas (id, titulo, artista, album, genero)
SELECT 3, 'Song 3', 'Artist 3', 'Album 3', '{rock}'
WHERE NOT EXISTS (SELECT 1 FROM Musicas WHERE id = 3);

-- Inserir preferências
INSERT INTO Preferencias (id, usuario_id, musica_id, avaliacao)
SELECT 1, 1, 1, 5
WHERE NOT EXISTS (SELECT 1 FROM Preferencias WHERE id = 1);

INSERT INTO Preferencias (id, usuario_id, musica_id, avaliacao)
SELECT 2, 1, 2, 4
WHERE NOT EXISTS (SELECT 1 FROM Preferencias WHERE id = 2);

INSERT INTO Preferencias (id, usuario_id, musica_id, avaliacao)
SELECT 3, 2, 3, 3
WHERE NOT EXISTS (SELECT 1 FROM Preferencias WHERE id = 3);
