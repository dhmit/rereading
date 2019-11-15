import React from 'react';
import ReactDOM from 'react-dom';

import 'bootstrap/dist/css/bootstrap.min.css';

import { PrototypeStudentView } from './prototype/student_view';
import { PrototypeInstructorView } from './prototype/instructor_view';
import { PrototypeAnalysisView } from './prototype/analysis_view';

import { ReadingView } from './views/reading_view';
import { ProjectView } from './views/overview_view';
import { AnalysisView } from './views/analysis_view';

window.app_modules = {
    React,  // Make React accessible from the base template
    ReactDOM,  // Make ReactDOM accessible from the base template

    // Add all frontend views here
    ReadingView,
    ProjectView,
    AnalysisView,

    // Prototype views
    PrototypeAnalysisView,
    PrototypeStudentView,
    PrototypeInstructorView,
};

