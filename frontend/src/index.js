import React from 'react';
import ReactDOM from 'react-dom';

import 'bootstrap/dist/css/bootstrap.min.css';

import StudentView from './views/student_view';
import InstructorView from './views/instructor_view';
import {AnalysisView} from './views/analysis_view';
import {DocumentAnalysisView} from "./views/document_analytics_view";
import ReadingView from './views/reading_view';

window.app_modules = {
    React,  // Make React accessible from the base template
    ReactDOM,  // Make ReactDOM accessible from the base template

    // Add all frontend views here
    StudentView,
    InstructorView,
    AnalysisView,
    ReadingView,
    DocumentAnalysisView,
};
