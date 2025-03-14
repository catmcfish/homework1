# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, flash, url_for
from .utils.database.database import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
import mysql.connector
import logging

# Create a logger
logger = logging.getLogger(__name__)

db = database()

@app.route('/')
def root():
    return redirect('/home')

@app.route('/home')
def home():
    try:
        x = random.choice(['I started university when I was a wee lad of 15 years.',
                          'I have a pet sparrow.',
                          'I write poetry.'])
        return render_template('home.html', fun_fact=x)
    except Exception as e:
        print(f"Error in home route: {e}")
        return render_template('home.html', fun_fact='')

@app.route('/resume')
def resume():
    try:
        resume_data = db.getResumeData()
        if not resume_data:
            flash('Unable to load resume data at this time.', 'error')
            return render_template('resume.html', resume_data={})
        return render_template('resume.html', resume_data=resume_data)
    except Exception as e:
        print(f"Error in resume route: {e}")
        flash('An error occurred while loading the resume.', 'error')
        return render_template('resume.html', resume_data={})

@app.route('/feedback')
def view_feedback():
    """Display all feedback submissions."""
    try:
        # Use direct SQL query instead of getFeedbackData method
        feedback_data = db.query("""
            SELECT 
                comment_id,
                name,
                email,
                comment,
                created_at,
                is_displayed
            FROM feedback
            ORDER BY created_at DESC
        """)
        return render_template('feedback.html', feedback_data=feedback_data)
    except Exception as e:
        print(f"Error retrieving feedback: {e}")
        flash('Unable to load feedback at this time. Error: ' + str(e), 'error')
        return redirect(url_for('home'))

@app.route('/processfeedback', methods=['POST'])
def process_feedback():
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        comment = request.form.get('comment')

        # Validate input
        if not all([name, email, comment]):
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('home'))

        # Insert feedback using direct SQL query
        try:
            query = "INSERT INTO feedback (name, email, comment) VALUES (%s, %s, %s)"
            db.query(query, [name, email, comment])
            flash('Thank you for your feedback!', 'success')
        except Exception as e:
            logger.error(f"Database error in feedback insertion: {e}", exc_info=True)
            flash('Unable to submit feedback at this time. Error: ' + str(e), 'error')
            return redirect(url_for('home'))

        return redirect(url_for('view_feedback'))

    except Exception as e:
        logger.error(f"Error in feedback submission: {e}", exc_info=True)
        flash('An error occurred while processing your feedback. Error: ' + str(e), 'error')
        return redirect(url_for('home'))
