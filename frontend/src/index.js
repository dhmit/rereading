import React from 'react';
import ReactDOM from 'react-dom';

import 'bootstrap/dist/css/bootstrap.min.css';

import StudentView from './prompted_readings/student_view';
import InstructorView from './prompted_readings/instructor_view';
import {AnalysisView} from './prompted_readings/analysis_view';

window.app_modules = {
    React,  // Make React accessible from the base template
    ReactDOM,  // Make ReactDOM accessible from the base template

    // Add all frontend views here
    StudentView,
    InstructorView,
    AnalysisView,
};
