import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

const PREFIX = process.env.REACT_APP_PREFIX || "/lab/frontend"


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <BrowserRouter basename={`${PREFIX}`}>
            <App />
        </BrowserRouter>
    </React.StrictMode>
);
