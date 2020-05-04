import psycopg2 as pg
from datetime import datetime


DATA = {
    'dbname': 'learningdb',
    'user': 'postgres',
    'password': '',
    'host': 'localhost',
    'port': '5432'
    }


def create_db():

    with pg.connect(**DATA) as conn:
        with conn.cursor() as curs:
            curs.execute("""CREATE TABLE student (
                    id serial PRIMARY KEY NOT NULL,
                    name varchar(100) NOT NULL,
                    gpa numeric(10, 2),
                    birth timestamp with time zone);
                    """)
            curs.execute("""CREATE TABLE course (
                    id serial PRIMARY KEY NOT NULL,
                    name varchar(100) NOT NULL);
                    """)
            curs.execute("""CREATE TABLE student_course (
                    id serial PRIMARY KEY,
                    student_id INTEGER REFERENCES student(id),
                    course_id INTEGER REFERENCES  course(id));
                    """)


def create_course():
    name = (input('Enter course name:'))
    with pg.connect(**DATA) as conn:
        with conn.cursor() as curs:
            curs.execute("insert into course (name) values (%s) RETURNING id", (name,))
            print('Course {} created with id: {}'.format(name, curs.fetchone()[0]))


def get_students(course_id):
    with pg.connect(**DATA) as conn:
        with conn.cursor() as curs:
            curs.execute("""select s.id, s.name, c.name from student_course sc
                        join student s on s.id = sc.student_id
                        join course c on c.id = sc.course_id
                        where c.id = %s
                        """, (course_id,))
            for row in curs:
                print('Course {} - student {} with id-{}'.format(row[2], row[1], row[0]))


def add_students(course_id, students):
    conn = pg.connect(**DATA)
    curs = conn.cursor()
    curs.execute("select * from course where id = %s", (course_id,))
    id_course = curs.fetchone()
    if id_course:
        for item in students:
            curs.execute("insert into student (name, gpa, birth) values (%s, %s, %s) RETURNING id",
                        (item.get('name'), item.get('gpa'), item.get('birth')))
            ids = curs.fetchone()
            curs.execute("insert into student_course (student_id, course_id) values (%s, %s)",
                        (ids, course_id))
        curs.close()
        conn.commit()
    else:
        print('Course with such ID not found\nCreate a course\n')
        return create_course()


def add_student(student):
    with pg.connect(**DATA) as conn:
        with conn.cursor() as curs:
            curs.execute("insert into student (name, gpa, birth) values (%s, %s, %s) RETURNING id",
                         (student.get('name'), student.get('gpa'), student.get('birth')))
            print('Student added')


def get_student(student_id):
    with pg.connect(**DATA) as conn:
        with conn.cursor() as curs:
            curs.execute("select * from student where id = %s", (student_id,))
            data = curs.fetchall()
            if data:
                for row in data:
                    print(f'ID: {row[0]}\nName: {row[1]}\ngpa: {row[2]}\nBithday: {datetime.date(row[3])}\n')
            else:
                print('Student with id:{} missing'.format(student_id))


if __name__ == '__main__':
    # create_db()
    # add_students(7, [{'name': 'Ivan', 'birth': '02.02.1980'},
    #                  {'name': 'John', 'gpa': '7', 'birth': '12.12.1990'}])
    # get_students(7)
    # get_student(1344)
    # add_student({'name': 'Mary', 'birth': '05.01.1984'})