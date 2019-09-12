import React from 'react';
import ReactDOM from 'react-dom';
import { Route, BrowserRouter as Router } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.min.css';

import Study from './prompted_readings/student_view';
import InstructorPage from './prompted_readings/instructor_view';

// note(ra): for sanity testing of django-webpack-loader...
// ReactDOM.render(<span>Hello, world!</span>, document.getElementById('root'));

function Hello() {
    return (
        <div>Hello, world!</div>
    )
}

const routing = (
    <Router>
        <div>
            <Route path="/" component={Hello} />
            <Route path="/student" component={Study} />
            <Route path="/instructor" component={InstructorPage} />
        </div>
    </Router>
);

ReactDOM.render(routing, document.getElementById('root'));
