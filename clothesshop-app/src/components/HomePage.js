import React, { useState, useEffect } from 'react';
import { Grid, Container, Typography, Box, Button } from '@mui/material';
import ProductCard from './ProductCard'; // Компонент карточки продукта
import axios from 'axios';
import images from './imagesLoader'; // Лоадер изображений

// Функция для выбора изображения на основе артикула
function getImageForProduct(article) {
    const articleString = String(article); // Приведение к строке
    let hash = 0;
    for (let i = 0; i < articleString.length; i++) {
        hash = articleString.charCodeAt(i) + ((hash << 5) - hash);
    }
    const index = Math.abs(hash % images.length); // Индекс в пределах массива `images`
    return images[index];
}


function HomePage({ addToCart }) {
    const [products, setProducts] = useState([]);
    const [categories, setCategories] = useState([]);
    const [filteredProducts, setFilteredProducts] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [showAllCategories, setShowAllCategories] = useState(false);

    // Загрузка товаров
    useEffect(() => {
        axios.get('/products')
            .then((response) => {
                const data = response.data;

                // Добавляем каждому товару картинку на основе артикула
                const productsWithImages = data.map((product) => ({
                    ...product,
                    image: getImageForProduct(product.article),
                }));

                setProducts(productsWithImages);
                setFilteredProducts(productsWithImages);
            })
            .catch((error) => {
                console.error('Ошибка загрузки товаров:', error);
            });
    }, []);

    // Загрузка категорий
    useEffect(() => {
        axios.get('/categories')
            .then((response) => {
                setCategories(response.data);
            })
            .catch((error) => {
                console.error('Ошибка загрузки категорий:', error);
            });
    }, []);

    // Фильтрация товаров по категории
    const handleFilter = (category) => {
        setSelectedCategory(category);

        const url = category ? `/products?category=${encodeURIComponent(category)}` : '/products';

        axios.get(url)
            .then((response) => {
                const data = response.data;
                const productsWithImages = data.map((product) => ({
                    ...product,
                    image: getImageForProduct(product.article),
                }));
                setFilteredProducts(productsWithImages);
            })
            .catch((error) => {
                console.error('Ошибка загрузки товаров с фильтром категории:', error);
            });
    };

    const visibleCategories = showAllCategories ? categories : categories.slice(0, 3);

    return (
        <Container style={{ marginTop: '20px' }}>
            <Typography variant="h4" gutterBottom>
                Каталог товаров
            </Typography>

            {/* Фильтр категорий */}
            <Box
                sx={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: '8px',
                    marginBottom: '20px',
                }}
            >
                <Button
                    variant={selectedCategory ? "outlined" : "contained"}
                    sx={{
                        backgroundColor: selectedCategory ? 'white' : '#b0bec5',
                        color: selectedCategory ? '#37474f' : 'white',
                        borderColor: '#37474f',
                        '&:hover': {
                            backgroundColor: selectedCategory ? '#eceff1' : '#90a4ae',
                        },
                    }}
                    onClick={() => handleFilter(null)}
                >
                    Все категории
                </Button>

                {visibleCategories.map((category, index) => (
                    <Button
                        key={index}
                        variant={selectedCategory === category ? "contained" : "outlined"}
                        sx={{
                            backgroundColor: selectedCategory === category ? '#37474f' : 'white',
                            color: selectedCategory === category ? 'white' : '#37474f',
                            borderColor: '#37474f',
                            '&:hover': {
                                backgroundColor: selectedCategory === category ? '#455a64' : '#eceff1',
                            },
                        }}
                        onClick={() => handleFilter(category)}
                    >
                        {category}
                    </Button>
                ))}
            </Box>

            {categories.length > 3 && (
                <Button
                    variant="outlined"
                    sx={{
                        borderColor: '#37474f',
                        color: '#37474f',
                        marginBottom: '20px',
                        '&:hover': {
                            backgroundColor: '#eceff1',
                        },
                    }}
                    onClick={() => setShowAllCategories((prev) => !prev)}
                >
                    {showAllCategories ? 'Скрыть категории' : 'Показать все категории'}
                </Button>
            )}

            {/* Список товаров */}
            <Grid container spacing={2}>
                {filteredProducts.map((product) => (
                    <Grid item xs={12} sm={6} md={4} key={product.article}>
                        <ProductCard
                            product_id={product.article}
                            name={product.name}
                            category={product.category}
                            stock={product.stock}
                            price={product.price}
                            image={product.image}
                        />
                    </Grid>
                ))}
            </Grid>
        </Container>
    );
}

export default HomePage;
