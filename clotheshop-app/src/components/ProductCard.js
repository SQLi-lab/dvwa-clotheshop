import React from 'react';
import { Card, CardContent, Typography, CardMedia, CardActionArea } from '@mui/material';
import { Link } from 'react-router-dom';

function ProductCard({ product_id, name, category, stock, price, image }) {
    return (
        <Card style={{ maxWidth: 300, margin: '10px', border: '1px solid #cfd8dc', borderRadius: '8px' }}>
            <CardActionArea component={Link} to={`/products/${product_id}`}>
                <CardMedia
                    component="img"
                    height="140"
                    image={image} // Используется картинка из `productsWithImages`
                    alt={name}
                    style={{ objectFit: 'contain', padding: '10px', backgroundColor: '#f5f5f5' }}
                />

                <CardContent>
                    <Typography variant="h6" component="div" style={{ color: '#37474f' }}>
                        {name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Категория: {category}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        В наличии: {stock > 0 ? `${stock} шт.` : 'Нет в наличии'}
                    </Typography>
                    <Typography variant="h6" color="text.primary" style={{ marginTop: '10px' }}>
                        {price} руб.
                    </Typography>
                </CardContent>
            </CardActionArea>
        </Card>
    );
}

export default ProductCard;
