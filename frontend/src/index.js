import React from 'react';
import ReactDOM from 'react-dom';

import './index.scss'

import { PrototypeStudentView } from './prototype/student_view';
import { PrototypeInstructorView } from './prototype/instructor_view';
import { PrototypeAnalysisView } from './prototype/analysis_view';

import { ReadingView } from './views/reading_view';
import { ReadingRedux } from './views/overview_view';
import { RereadingSample } from './views/overview_view';
import { RereadingVisuals } from './views/overview_view';
import { RereadingValues } from './views/overview_view';
import { QuantitativeQuestions } from './views/overview_view';
import { Sources } from './views/overview_view';

import { AnalysisView } from './views/analysis_view';
window.app_modules = {
    React,  // Make React accessible from the base template
    ReactDOM,  // Make ReactDOM accessible from the base template

    // Add all frontend views here
    ReadingView,
    AnalysisView,
    ReadingRedux,
    RereadingSample,
    RereadingVisuals,
    RereadingValues,
    QuantitativeQuestions,
    Sources,


    // Prototype views
    PrototypeAnalysisView,
    PrototypeStudentView,
    PrototypeInstructorView,
};

