-- 1. Список всех людей (Выборка списков)
SELECT id, name FROM people ORDER BY name;

-- 2. Список всех подарков с именами людей (JOIN)
SELECT gifts.idea, people.name AS person_name, gifts.is_done
FROM gifts
JOIN people ON gifts.person_id = people.id;

-- 3. Поиск людей по имени (Фильтрация WHERE)
SELECT id, name FROM people WHERE name LIKE '%Иван%';

-- 4. Поиск подарков для конкретного человека (Фильтрация WHERE)
SELECT idea FROM gifts WHERE person_id = 1;

-- 5. Полная информация о подарке (JOIN)
SELECT gifts.idea, people.name AS person_name, events.title AS event_title, events.date
FROM gifts
JOIN people ON gifts.person_id = people.id
JOIN events ON gifts.event_id = events.id;

-- 6. Все события с именами людей (JOIN)
SELECT events.title, events.date, people.name AS person_name
FROM events
JOIN people ON events.person_id = people.id;

-- 7. Количество всех подарков (Агрегатная функция)
SELECT COUNT(*) AS total_gifts FROM gifts;

-- 8. Количество вручённых подарков (Агрегатная функция + WHERE)
SELECT COUNT(*) AS done_gifts FROM gifts WHERE is_done = 1;

-- 9. Статистика: сколько подарков у каждого человека (GROUP BY)
SELECT people.name, COUNT(gifts.id) AS gifts_count
FROM people
LEFT JOIN gifts ON people.id = gifts.person_id
GROUP BY people.id, people.name;

-- 10. Люди, у которых больше 1 подарка (GROUP BY + HAVING)
SELECT people.name, COUNT(gifts.id) AS gifts_count
FROM people
JOIN gifts ON people.id = gifts.person_id
GROUP BY people.id, people.name
HAVING COUNT(gifts.id) > 1;