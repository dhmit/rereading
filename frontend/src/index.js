import React from 'react';
import ReactDOM from 'react-dom';

import { PrototypeStudentView } from './prototype/student_view';

import { PrototypeInstructorView } from './prototype/instructor_view';
import { PrototypeAnalysisView } from './prototype/analysis_view';
import { ReadingView } from './views/reading_view';

import { LandingPageView } from './views/landing_page';
import {
    ReadingRedux,
    RereadingSample,
    RereadingVisuals,
    RereadingValues,
    QuantitativeQuestions,
    Sources,
    Writeups,
} from './views/overview_view';

import { AnalysisView } from './views/analysis_view';

import './index.scss'

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
    Writeups,
    LandingPageView,

    // Prototype views
    PrototypeAnalysisView,
    PrototypeStudentView,
    PrototypeInstructorView,
};

