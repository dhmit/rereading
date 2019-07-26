import React from 'react';
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.min.css';

import Study from './App';
import InstructorPage from './instructor_data_view';

// note(ra): for sanity testing of django-webpack-loader...
// ReactDOM.render(<span>Hello, world!</span>, document.getElementById('root'));

const routing = (
    <Router>
        <div>
            <Route path="/" component={Study} />
            <Route path="/instructor" component={InstructorPage} />
        </div>
    </Router>
);

ReactDOM.render(routing,document.getElementById('root'));
