const express = require('express');
const app = express();
const port = 3000;
const { Pool } = require('pg');

const pool = new Pool({
  user: 'postgres',     
  host: 'localhost',         
  database: 'postgres', 
  password: 'a', 
  port: 5432,       
});

// Middleware to parse JSON
app.use(express.json());

// Sample route
app.get('/', (req, res) => {
    res.send('Hello, world!');
});


app.get('/data', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM sensor_data WHERE room_name = "Q4-1003"');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
});


app.get('/data/q4-1003', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM sensor_data WHERE room_name = "Q4-1003"');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
});

// Sample API endpoint
app.get('/api/data', (req, res) => {
    const sampleData = {
        id: 1,
        name: 'Sample Data'
    };
    res.json(sampleData);
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});


let items = [];


// Create
app.post('/api/items', (req, res) => {
    const newItem = req.body;
    newItem.id = items.length + 1;
    items.push(newItem);
    res.status(201).json(newItem);
});

// Read
app.get('/api/items', (req, res) => {
    res.json(items);
});

// Read by ID
app.get('/api/items/:id', (req, res) => {
    const item = items.find(i => i.id == req.params.id);
    if (item) {
        res.json(item);
    } else {
        res.status(404).send('Item not found');
    }
});

// Update
app.put('/api/items/:id', (req, res) => {
    const item = items.find(i => i.id == req.params.id);
    if (item) {
        Object.assign(item, req.body);
        res.json(item);
    } else {
        res.status(404).send('Item not found');
    }
});

// Delete
app.delete('/api/items/:id', (req, res) => {
    items = items.filter(i => i.id != req.params.id);
    res.status(204).send();
});
