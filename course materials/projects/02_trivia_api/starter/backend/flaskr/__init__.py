import os, sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

'''
Create and setup flask app and init db
'''
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # CORS Headers 
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  '''
  Endpoint to handle GET requests for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    #take all categories from DB and format them
    categories=get_category_list()
    return jsonify({
      'success':True,
      'categories':categories,
      'total_categories':len(categories)
    })
  '''
  Helper code to assist in loading quesitons
  '''
  def paginate_questions(request, questions_list):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in questions_list]

    paginated_questions = questions[start:end]

    return paginated_questions

  def get_category_list():
      categories = {}
      for category in Category.query.all():
        categories[category.id] = category.type
      return categories

  '''
  Endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''
  @app.route('/questions',methods=['GET'])
  def get_questions():
    '''
    Get all questions
    '''
    try:
      # paginate questions, and store the current page questions in a list
      questions_list = Question.query.all()
      selection = paginate_questions(request, questions_list)
      total_questions = len(selection)
      
      if total_questions == 0:
          # no questions are found, abort with a 404 error.
          abort(404)
      
      return jsonify({
          'success': True,
          'questions': selection,
          'total_questions': total_questions,
          'categories': get_category_list(),
          'current_category': None
      })
    except:
      print(sys.exc_info())

  '''
  Create an endpoint to DELETE question using a question ID. 
  '''
  @app.route('/questions/<question_id>', methods=['Delete'])
  def delete_question(question_id):
    '''Delete a question from the database'''
    try:
        question = Question.query.filter(Question.id == question_id).one_or_none()
        # return 404 if question is not available
        if question is None:
            abort(404)
        
        question.delete()
        
        return jsonify({
            'success': True,
            'deleted': question_id
        })
    except:
        # rollback and close the connection
        print(sys.exc_info())
        db.session.rollback()
        abort(422)

  '''
  Endpoint to POST a new question, 
  which will require the question and answer text, category, and difficulty score.
  '''
  @app.route('/questions', methods=['POST'])
  def create_questions():
    try:
      request_body = request.get_json()
      # needs to have a body 
      if not request_body:
        abort(400)
      # extract data from body for question
      new_question = Question(
          request_body['question'],
          request_body['answer'],
          request_body['category'],
          request_body['difficulty']
      )
      # QA check on difficulty
      if not 1 <= int(request_body['difficulty']) < 6:
        abort(400)
      # validating that the quesiton and answer must be present
      if request_body['question'] == '' or request_body['answer'] == '':
        raise TypeError
      # insert the new question
      new_question.insert()

      return jsonify({
          'success': True
      }), 201

    except TypeError:
      print(sys.exc_info())
      abort(422)

    except:
      print(sys.exc_info())
      abort(500)


  '''
  Endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    request_body = request.get_json()
    search_term = request_body.get('searchTerm')
    current_category = request_body.get('current_category') 
    
    if not request_body:
      # body should have valid json
      print(sys.exc_info())
      abort(400)

    if search_term: 
      #query db for the paginated results
      page = request.args.get('page', 1, type=int)
      results = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).paginate(page, QUESTIONS_PER_PAGE, True)
      total_questions = results.total
      
      if total_questions == 0:
        # no questions returned from db
        print(sys.exc_info())
        abort(404)
      
      current_questions = [question.format() for question in results.items]
      
      return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'searchTerm': search_term
        }), 200
    else: 
      # if no search term no search
      print(sys.exc_info())
      abort(400)


  ''' 
  Endpoint to get questions based on category. 
  '''
  @app.route('/categories/<category_id>/questions', methods=['GET'])
  def search_questions_by_category(category_id):
    '''Get all questions in a category'''
    # category = Category.query.filter(Category.id == category_id).one_or_none()
    # if category is None:
    #   # abort is category is none
    #   abort(404)
    # # paginate questions, and store the current page questions in a list
    # page = request.args.get('page', 1, type=int)
    # results = Question.query.filter(Question.category == category.id).order_by(Question.id).paginate(page, QUESTIONS_PER_PAGE, True)

    # total_questions = results.total
    # current_questions = [question.format() for question in results.items]

    # return jsonify(
    #   {
    #     'success':True,
    #     'questions':current_questions,
    #     'total_questions': total_questions,
    #     'current_category': category.type
    #   }
    # ), 200
    try:
      questions_search_term = request.args.get('searchTerm', '')
      questions_query = Question.query.filter(
          Question.category == category_id,
          Question.question.ilike("%{}%".format(questions_search_term))
      ).order_by(Question.id).all()
      questions_data = [question.format() for question in questions_query]

      if len(questions_data) == 0:
          raise IndexError

      categories_query = Category.query.order_by(Category.id).all()
      categories_data = {}

      for category in categories_query:
          categories_data[category.id] = category.type

      return jsonify({
          'questions': questions_data[:QUESTIONS_PER_PAGE],
          'total_questions': len(questions_data),
          'categories': categories_data,
          'current_category': category_id,
          'search_term': questions_search_term
      }), 200

    except IndexError:
      print(sys.exc_info())
      abort(404)

    except:
      print(sys.exc_info())
      abort(500)


  '''
  Endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    '''take a quiz in the trivia game'''
    # load the request body
    body = request.get_json()
    if not body:
        # posting an envalid json should return a 400 error.
        abort(400)
    if (body.get('previous_questions') is None or body.get('quiz_category') is None):
        # if previous_questions or quiz_category are missing, return a 400 error
        abort(400)
    previous_questions = body.get('previous_questions')
    if type(previous_questions) != list:
        # previous_questions should be a list, otherwise return a 400 error
        abort(400)
    category = body.get('quiz_category')
    # just incase, convert category id to integer
    category_id = int(category['id'])
    # insure that there are questions to be played.
    if category_id == 0:
        # if category id is 0, query the database for a random object of all questions
        selection = Question.query.order_by(func.random())
    else:
        # load a random object of questions from the specified category
        selection = Question.query.filter(
            Question.category == category_id).order_by(func.random())
    if not selection.all():
        # No questions available, abort with a 404 error
        abort(404)
    else:
        # load a random question from our previous query, which is not in the previous_questions list.
        question = selection.filter(Question.id.notin_(
            previous_questions)).first()
    if question is None:
        # all questions were played, returning a success message without a question signifies the end of the game
        return jsonify({
            'success': True
        })
    # Found a question that wasn't played before, let's return it to the user
    return jsonify({
        'success': True,
        'question': question.format()
    })




  '''
  Error handlers for all expected errors 
  '''
  @app.errorhandler(400)
  @app.errorhandler(404)
  @app.errorhandler(405)
  @app.errorhandler(422)
  @app.errorhandler(500)
  def error_handler(error):
      return jsonify({
          'success': False,
          'error': error.code,
          'message': error.description
      }), error.code
  
  return app

    