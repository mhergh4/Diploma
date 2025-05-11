
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("USE my_shop;")

        for tag in tags:
            cursor.execute("""
                INSERT INTO preferences_tags (user_id, tag, weight, last_interaction)
                VALUES (%s, %s, 1, NOW())
                ON DUPLICATE KEY UPDATE
                weight = weight + 1,
                last_interaction = NOW()
            """, (user_id, tag.lower()))

        conn.commit()
        cursor.close()