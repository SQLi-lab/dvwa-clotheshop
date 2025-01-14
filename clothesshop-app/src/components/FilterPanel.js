import React from 'react';
import { Button, Stack } from '@mui/material';

function FilterPanel({ categories, onFilter }) {
    return (
        <Stack direction="row" spacing={2} style={{ marginBottom: '20px' }}>
            {categories.map((category) => (
                <Button
                    key={category}
                    variant="contained"
                    onClick={() => onFilter(category)}
                >
                    {category}
                </Button>
            ))}
        </Stack>
    );
}

export default FilterPanel;
