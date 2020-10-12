import React, { Component } from 'react';
import $ from 'jquery';
import * as Constants from '../common/constants';

import '../stylesheets/FormView.css';
import '../stylesheets/bootstrap.min.css';

class FormView extends Component {
  constructor(props){
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: {}
    }
  }

  componentDidMount(){
    $.ajax({
      url: `${Constants.SERVERPATH}/categories`, // update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try again.')
        return;
      }
    })
  }

  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: `${Constants.SERVERPATH}/questions`, // update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-question-form").reset();
        return;
      },
      error: (error) => {
        alert('Unable to add the question. Please try again.')
        return;
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  render() {
    return (
      <div id="add-form">
        <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
          <div class="container">
            <div class="row">
              <div class="col-md-9 col-md-offset-3 text-center">
              <h2>Add a New Trivia Question</h2>
                <div class="form-group">
                  <label>Question</label>
                  <input type="text" class="form-control" name="question" onChange={this.handleChange}/>
                </div>
                <div class="form-group">
                  <label>Answer</label>
                  <input type="text" class="form-control" name="answer" onChange={this.handleChange}/>
                </div>
                <div class="form-group">
                  <label>Difficulty</label>
                  <select class="form-control" name="difficulty" onChange={this.handleChange}>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Category</label>
                  <select class="form-control" name="category" onChange={this.handleChange}>
                    {Object.keys(this.state.categories).map(id => {
                      return (
                        <option key={id} value={id}>{this.state.categories[id]}</option>
                      )
                    })}
                  </select>
                </div>
                <input type="submit" className="button" value="Submit" />
              </div>
            </div>
          </div>
        </form>
      </div>
    );
  }
}

export default FormView;