import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}" .format(
            'postgres',os.environ.get('PSQL_PASS'),'localhost:5432', self.database_name
            )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        # pop the app context
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        '''
        Test getting all categories
        '''
        # get response json, then load the data
        response = self.client().get('/categories')
        data = json.loads(response.data)
        # status code should be 200 (SUCCESS)
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # categories should be present
        self.assertTrue(data['categories'])
        # categories length should be more than 0
        self.assertGreater(len(data['categories']), 0)

    def test_get_questions(self):
        '''
        Tests getting questions
        '''
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        # status code should be 200 (SUCCESS)
        self.assertEqual(res.status_code, 200)
        # categories length should be more than 0
        self.assertTrue(len(data['questions']))
        # categories length should be more than 0
        self.assertTrue(data['total_questions'])
        # categories length should be more than 0
        self.assertTrue(data['categories'])

    def test_create_questions(self):
        '''
        TEST: When you submit a question on the "Add" tab, 
        the form will clear and the question will appear at the end of the last page
        of the questions list in the "List" tab. 
        '''
        new_question={
            'question': 'new question',
            'answer': 'new answer',
            'difficulty': 3,
            'category': 1
            }
        # get response json, then load the data
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        # status code should be 201
        self.assertEqual(response.status_code, 201)
        # success should be true
        self.assertTrue(data['success'])

    def test_search_questions(self):
        '''
        TEST: Search by any phrase. The questions list will update to include 
        only question that include that string within their question. 
        Try using the word "title" to start. 
        '''
        search_term = {'search_term': 'title'}
        # get response json, then load the data
        response = self.client().post('/questions/search',json=search_term)
        data = json.loads(response.data)
        # success should be true
        self.assertTrue(data['success'])
        # questions and total_questions should be present in data
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        # questions and total_questions length should be more than 0
        self.assertGreater(len(data['questions']), 0)
        self.assertGreater(data['total_questions'], 0)
        # total_questions should be an integer
        self.assertEqual(type(data['total_questions']), int)
    
    def test_search_questions_by_category(self):
        '''
        TEST: In the "List" tab / main screen, clicking on one of the 
        categories in the left column will cause only questions of that 
        category to be shown. 
        '''
        # get the first random category from db
        category = Category.query.order_by(func.random()).first()
        # get response json, then load the data
        response = self.client().get(
            f'/categories/{category.id}/questions')
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # questions and total_questions should be present
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        # questions and total_questions length should be more than 0
        self.assertGreater(len(data['questions']), 0)
        self.assertGreater(data['total_questions'], 0)
        # total_questions should be an integer
        self.assertEqual(type(data['total_questions']), int)
        # current_category equals to category.type
        self.assertEqual(data['current_category'], category.type)
        # for each question, category id should be the same id from db
        for question in data['questions']:
            self.assertEqual(question['category'], category.id)

    def test_play_quiz(self):
        '''
        TEST: In the "Play" tab, after a user selects "All" or a category,
        one question at a time is displayed, the user is allowed to answer
        and shown whether they were correct or not. 
        '''
        # query db for 2 random questions
        questions = Question.query.order_by(func.random()).limit(2).all()
        previous_questions = [question.id for question in questions]
        # post response json, then load the data
        response = self.client().post('/quizzes', json={
            'previous_questions': previous_questions,
            'quiz_category': {'id': 2}
        })
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # question should be present
        self.assertTrue(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()