const express = require("express")
const multer = require("multer")
const sharp = require("sharp")
const path = require("path")

const app = express()
const PORT = 1234
const upload = multer()

app.get("/", (req, res) => {
    res.status(200)
    res.sendFile(path.join(__dirname+"/form.html"))
})

app.get("/login", (req, res) => {
    res.status(200)
    res.json({author: "1155288"})
})

app.post("/size2json", upload.single('image'), async (req, res) => {
    try{
        const image = req.file.file
        const image_link = sharp(req.file.buffer)
        const metadata = await image.metadata()

        res.status(200).json({width: metadata.width, height: metadata.height})
    } catch(err){
        res.status(415).json({result: "invalid filetype"})
    }
})

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`)
})