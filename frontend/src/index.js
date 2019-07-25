import React from 'react';
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom';
import './index.css';
import Study from './App';
import InstructorPage from './instructor_data_view';
import * as serviceWorker from './serviceWorker';

// ReactDOM.render(<Study />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
// serviceWorker.unregister();

const routing = (
    <Router>
        <div>
            <Route path="/student" component={Study} />
            <Route path="/instructor" component={InstructorPage} />
        </div>
    </Router>
)

ReactDOM.render(routing,document.getElementById('root'))