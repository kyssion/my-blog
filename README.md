SELECT 
    scope,
    scope_name,
    scope_level,
    scope_type,
    master,
    status,
    role_key
FROM
    (SELECT 
        *
    FROM
        pri_user_scope
    WHERE
        (scope LIKE '0/%' OR scope = '0')
            AND status = 1
            AND scope_type = 2
            AND scope_level = 2) o,
    (SELECT 
        role_key, user_id
    FROM
        pri_user_role
    WHERE
        role_key = 'operate_region_2') p
WHERE
    o.user_id = p.user_id
GROUP BY scope;