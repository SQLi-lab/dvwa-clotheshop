import React, { useState, useEffect } from 'react';
import BACKEND_URL from './Constants';
import { useNavigate } from 'react-router-dom';
import profileImage from './profile_pictures/profile.png';

import {
    Container,
    TextField,
    Button,
    Typography,
    Paper,
    Snackbar,
    Pagination,
    Grid,
    Box
} from '@mui/material';

// Функция для извлечения куки по имени
function getCookieByName(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(`${name}=`)) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

function ProfilePage() {
    const navigate = useNavigate();
    useEffect(() => {
        const isLoggedIn = localStorage.getItem('loggedIn') === 'true';
        const userCookie = document.cookie.split(';').find((cookie) => cookie.trim().startsWith('user='));

        if (!isLoggedIn || !userCookie) {
            navigate('/login');
        }
    }, [navigate]);

    const [userData, setUserData] = useState({
        username: '',
        name: '',
        passport: '',
        birthDate: '',
        address: '',
        phone: '',
        description: '',
    });
    const [isEditing, setIsEditing] = useState(false);
    const [newDescription, setNewDescription] = useState('');
    const [orders, setOrders] = useState([]);
    const [favorites, setFavorites] = useState([]); // Для любимых машин
    const [reviews, setReviews] = useState([]);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    const [currentPage, setCurrentPage] = useState(1);
    const [currentReviewsPage, setCurrentReviewsPage] = useState(1);

    const itemsPerPage = 5;

    useEffect(() => {
        const fetchUserReviews = async () => {
            try {
                const userCookie = getCookieByName('user');
                const response = await fetch(`${BACKEND_URL}/profile/reviews`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + userCookie,
                    },
                });
                if (!response.ok) throw new Error('Ошибка загрузки отзывов пользователя');
                const data = await response.json();
                setReviews(data || []);
            } catch (error) {
                console.error('Ошибка загрузки отзывов пользователя:', error);
            }
        };

        fetchUserReviews();
    }, []);


    useEffect(() => {
        const userCookie = getCookieByName('user');

        fetch(`${BACKEND_URL}/orders`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + userCookie,
            },
        })
            .then((response) => response.json())
            .then((data) => {
                setOrders(data); // Устанавливаем заказы из API
            })
            .catch((error) => {
                console.error('Ошибка получения заказов:', error);
            });
    }, []);

    useEffect(() => {
        fetch(`${BACKEND_URL}/profile/favorites`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getCookieByName('user'),
            },
        })
            .then((response) => response.json())
            .then((data) => {
                setFavorites(data.favorites || []);
            })
            .catch((error) => console.error('Ошибка получения избранных машин:', error));
    }, []);

    useEffect(() => {
        fetch(`${BACKEND_URL}/profile`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getCookieByName('user'),
            },
        })
            .then((response) => response.json())
            .then((data) => {
                setUserData({
                    username: data.username,
                    name: data.name,
                    passport: data.passport || '',
                    birthDate: data.birthDate || '',
                    address: data.address || '',
                    phone: data.phone || '',
                    description: data.description || '',
                });
                setNewDescription(data.description || '');
            })
            .catch((error) => {
                console.error('Ошибка получения профиля:', error);
            });
    }, []);

    const showMessage = (message) => {
        setSnackbarMessage(message);
        setSnackbarOpen(true);
    };

    const handleSnackbarClose = () => {
        setSnackbarOpen(false);
    };

    const handleEdit = () => {
        setIsEditing(true);
    };

    const handleSave = () => {
        const userCookie = getCookieByName('user');

        if (!userCookie) {
            console.error('Кука "user" не найдена!');
            return;
        }

        fetch(`${BACKEND_URL}/profile`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + userCookie,
            },
            body: JSON.stringify({ description: newDescription }),
        })
            .then((response) => response.json())
            .then(() => {
                setUserData((prevData) => ({ ...prevData, description: newDescription }));
                setIsEditing(false);
                showMessage('Описание успешно обновлено!');
            })
            .catch((error) => {
                console.error('Ошибка сохранения описания:', error);
            });
    };

    const paginatedOrders = orders.slice(
        (currentPage - 1) * itemsPerPage,
        currentPage * itemsPerPage
    );

    const paginatedReviews = reviews.slice(
        (currentReviewsPage - 1) * itemsPerPage,
        currentReviewsPage * itemsPerPage
    );

    const handlePageChange = (event, value) => {
        setCurrentPage(value);
    };

    const handleReviewsPageChange = (event, value) => {
        setCurrentReviewsPage(value);
    };

    return (
        <Container style={{ marginTop: '20px', fontFamily: 'Arial, sans-serif' }}>
            <Paper elevation={3} style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
                <Typography variant="h5" style={{ textAlign: 'center', marginBottom: '20px' }}>
                    {userData.username}
                </Typography>

                {/* Блок с информацией о пользователе */}
                <Paper elevation={2} style={{ padding: '20px', marginBottom: '20px' }}>
                    <Grid container spacing={2}>
                        <Grid item xs={12} md={3} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                            <img
                                src={profileImage}
                                alt="Аватар пользователя"
                                style={{ borderRadius: '50%', width: '150px', height: '150px' }}
                            />
                        </Grid>
                        <Grid item xs={12} md={9}>
                            <Typography variant="h6">{userData.name}</Typography>
                            <Typography>Паспорт: {userData.passport}</Typography>
                            <Typography>Дата рождения: {userData.birthDate}</Typography>
                            <Typography>Адрес: {userData.address}</Typography>
                            <Typography>Телефон: {userData.phone}</Typography>
                        </Grid>
                    </Grid>
                </Paper>

                {/* Любимые машины */}
                <Paper elevation={2} style={{ padding: '20px', marginBottom: '20px' }}>
                    <Typography variant="h6" style={{ marginBottom: '10px' }}>
                        Любимые машины:
                    </Typography>
                    {favorites.length === 0 ? (
                        <Typography>У вас нет любимых машин</Typography>
                    ) : (
                        favorites.map((fav, index) => (
                            <Typography key={index}>{fav.car_name}</Typography>
                        ))
                    )}
                </Paper>

                {/* Блок "Ваши заказы" */}
                <Paper elevation={2} style={{ padding: '20px', marginBottom: '20px' }}>
                    <Typography variant="h6" style={{ marginBottom: '10px' }}>
                        Ваши заказы:
                    </Typography>
                    {paginatedOrders.length === 0 ? (
                        <Typography>У вас нет заказов</Typography>
                    ) : (
                        <>
                            {paginatedOrders.map((order, index) => (
                                <Paper
                                    key={index}
                                    elevation={1}
                                    style={{ padding: '10px', marginBottom: '10px', border: '1px solid #ccc' }}
                                >
                                    <Grid container>
                                        <Grid item xs={4}>
                                            <Typography style={{ fontWeight: 'bold' }}>Автомобиль:</Typography>
                                            <Typography>{order.model_name}</Typography>
                                        </Grid>
                                        <Grid item xs={4}>
                                            <Typography style={{ fontWeight: 'bold' }}>Цена:</Typography>
                                            <Typography>{order.price} руб.</Typography>
                                        </Grid>
                                        <Grid item xs={4}>
                                            <Typography style={{ fontWeight: 'bold' }}>Статус:</Typography>
                                            <Typography>{order.status}</Typography>
                                        </Grid>
                                    </Grid>
                                </Paper>
                            ))}
                            {orders.length > itemsPerPage && (
                                <Pagination
                                    count={Math.ceil(orders.length / itemsPerPage)}
                                    page={currentPage}
                                    onChange={handlePageChange}
                                    style={{ marginTop: '10px' }}
                                />
                            )}
                        </>
                    )}
                </Paper>

                {/* Блок "Отзывы" */}
                <Paper elevation={2} style={{ padding: '20px', marginBottom: '20px' }}>
                    <Typography variant="h6" style={{ marginBottom: '10px' }}>
                        Ваши отзывы:
                    </Typography>
                    {reviews.length === 0 ? (
                        <Typography>Вы еще не оставили отзывы</Typography>
                    ) : (
                        reviews.map((review, index) => (
                            <Paper
                                key={index}
                                elevation={1}
                                style={{ padding: '10px', marginBottom: '10px', border: '1px solid #ccc' }}
                            >
                                <Typography style={{ fontWeight: 'bold' }}>Автомобиль:</Typography>
                                <Typography>{review.car_name}</Typography>
                                <Typography style={{ fontWeight: 'bold', marginTop: '5px' }}>Отзыв:</Typography>
                                <Typography>{review.review_text}</Typography>
                                <Typography style={{ fontSize: '0.8em', color: '#777', marginTop: '5px' }}>
                                    Дата: {review.review_date}
                                </Typography>
                            </Paper>
                        ))
                    )}
                </Paper>

            </Paper>

            <Snackbar
                open={snackbarOpen}
                autoHideDuration={3000}
                onClose={handleSnackbarClose}
                message={snackbarMessage}
            />
        </Container>
    );
}

export default ProfilePage;
