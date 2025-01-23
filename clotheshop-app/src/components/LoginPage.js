import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, TextField, Button, Alert, Typography } from '@mui/material';
import BACKEND_URL from './Constants';
import axios from 'axios';

axios.defaults.withCredentials = true;
axios.defaults.baseURL = `${BACKEND_URL}`; // Базовый URL бэкенда

function LoginPage({ setLoggedIn }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null); // Для отображения ошибок
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            setError(null); // Сбрасываем ошибку перед новой попыткой входа
            const response = await axios.post('/login', {
                username,
                password,
            });

            console.log(response.data.message); // Успешный вход
            setLoggedIn(true); // Устанавливаем статус входа
            navigate('/'); // Возвращаемся на главную страницу
        } catch (error) {
            if (error.response) {
                // Если сервер вернул ответ с ошибкой
                console.error('Ошибка:', error.response.data.message);
                setError(error.response.data.message);
            } else {
                // Если произошла сетевая ошибка или что-то другое
                console.error('Сетевая ошибка или другая проблема:', error.message);
                setError('Произошла ошибка. Попробуйте позже.');
            }
        }
    };

    return (
        <Container
            style={{
                marginTop: '50px',
                textAlign: 'center',
                maxWidth: '400px',
                padding: '20px',
                backgroundColor: '#f5f5f5',
                borderRadius: '10px',
            }}
        >
            <Typography variant="h4" style={{ marginBottom: '20px', color: '#37474f' }}>
                Авторизация
            </Typography>
            {error && (
                <Alert severity="error" style={{ marginBottom: '20px' }}>
                    {error}
                </Alert>
            )}
            <TextField
                label="Логин"
                variant="outlined"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                fullWidth
                style={{ marginBottom: '20px' }}
                sx={{
                    '& .MuiOutlinedInput-root': {
                        '& fieldset': {
                            borderColor: '#37474f',
                        },
                        '&:hover fieldset': {
                            borderColor: '#90a4ae',
                        },
                        '&.Mui-focused fieldset': {
                            borderColor: '#37474f',
                        },
                    },
                    '& .MuiInputLabel-root': {
                        color: '#37474f',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                        color: '#37474f',
                    },
                }}
            />
            <TextField
                label="Пароль"
                type="password"
                variant="outlined"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                fullWidth
                style={{ marginBottom: '20px' }}
                sx={{
                    '& .MuiOutlinedInput-root': {
                        '& fieldset': {
                            borderColor: '#37474f',
                        },
                        '&:hover fieldset': {
                            borderColor: '#90a4ae',
                        },
                        '&.Mui-focused fieldset': {
                            borderColor: '#37474f',
                        },
                    },
                    '& .MuiInputLabel-root': {
                        color: '#37474f',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                        color: '#37474f',
                    },
                }}
            />
            <Button
                variant="contained"
                style={{
                    backgroundColor: '#37474f',
                    color: '#fff',
                    padding: '10px 20px',
                }}
                onClick={handleLogin}
                disabled={!username || !password}
            >
                Войти
            </Button>
        </Container>
    );
}

export default LoginPage;
