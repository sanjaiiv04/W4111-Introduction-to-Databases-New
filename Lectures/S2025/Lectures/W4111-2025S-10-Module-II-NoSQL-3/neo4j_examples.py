from neo4j import GraphDatabase

class Neo4jMoviesApp:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_sample_queries(self):
        with self.driver.session() as session:
            print("\n🎬 All Movies:")
            session.read_transaction(self._print_all_movies)

            print("\n⭐ Actors and Roles for 'The Matrix':")
            session.read_transaction(self._print_actors_for_movie, "The Matrix")

            print("\n🎥 Movies acted in by 'Tom Hanks':")
            session.read_transaction(self._print_movies_by_actor, "Tom Hanks")

    @staticmethod
    def _print_all_movies(tx):
        query = "MATCH (m:Movie) RETURN m.title AS title ORDER BY title"
        result = tx.run(query)
        for record in result:
            print(f"- {record['title']}")

    @staticmethod
    def _print_actors_for_movie(tx, movie_title):
        query = """
        MATCH (a:Person)-[r:ACTED_IN]->(m:Movie {title: $title})
        RETURN a.name AS actor, r.roles AS roles
        ORDER BY actor
        """
        result = tx.run(query, title=movie_title)
        for record in result:
            roles = ', '.join(record['roles']) if record['roles'] else "N/A"
            print(f"- {record['actor']} as {roles}")

    @staticmethod
    def _print_movies_by_actor(tx, actor_name):
        query = """
        MATCH (p:Person {name: $name})-[:ACTED_IN]->(m:Movie)
        RETURN m.title AS title
        ORDER BY m.title
        """
        result = tx.run(query, name=actor_name)
        for record in result:
            print(f"- {record['title']}")


if __name__ == "__main__":
    # Update these credentials as needed
    uri = "bolt://localhost:7687"
    user = "dbuser"
    password = "dbuserdbuser"

    app = Neo4jMoviesApp(uri, user, password)
    try:
        app.print_sample_queries()
    finally:
        app.close()
