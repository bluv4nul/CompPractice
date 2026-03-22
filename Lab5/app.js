const express = require('express')

const PORT = 3000
const app = express()

let notes = [];

app.use(express.json())

app.get("/", (req, res) => {
    res.status(200).json("Main Paige")
})

app.get("/notes", (req, res) => {
    if (notes.length == 0){
        res.status(200).json("No notes yet")
    } else { 
        res.status(200).json(notes)
    }
})

app.post("/notes/add", (req, res) => {
    try{
        const { text } = req.body

        if(!text){
            res.status(400).json("Field 'text' required")
        }

        const note = {
            id: notes.length + 1,
            text: text
        }

        notes.push(note)

        res.status(201).json({message: "Succesfull", note: note})
    } catch (err) {
        res.status(500).json({message: "Internal Server Error"})
    }
})

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`)
})



