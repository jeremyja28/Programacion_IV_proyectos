
-- Update password hashes with correct values
UPDATE usuarios SET password_hash = 'scrypt:32768:8:1$NkP6GnJeRyuGHKe3$e8a68007034cc2cd1d1b5a4466cb180aff89e086c1f2b7d1c52a37143d74794429d29dcfc7c8d255566625b1183d3a2288a17193b5b9723d90e2d91a88f319bd' WHERE username = 'admin';
UPDATE usuarios SET password_hash = 'scrypt:32768:8:1$OJikBuSMKTszB04E$3a37c9076b0732abcb8692f374c5d84d2a455bd919dcb313259605345c9bbf2c2ab6101c756770b02898e02e7bbcbe03dc31f0db7d6672985ce23e10ce85ac37' WHERE username = 'usuario';

-- Verify updates
SELECT username, LEFT(password_hash, 20) as hash_preview FROM usuarios;
