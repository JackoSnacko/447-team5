
import React, {useState, useEffect} from 'react'
import APIService from './APIService'

function Form(props) {
    const [name, setName] = useState('')
    const [id, setId] = useState('')
    const [points, setPoints] = useState('')

    useEffect(() => {
        setName(props.student.name)
        setId(props.student.id)
        setPoints(props.student.points)
    },[props.student])


    const updateStudent = () => {
        APIService.UpdateStudent(props.student.data_id, {name, id, points})
        .then(resp => props.updatedData(resp))
        .catch(error => console.log(error))
    }

    const insertStudent = () => {
        APIService.InsertStudent({name, id, points})
        .then(resp => props.insertedStudent(resp))
        .catch(error => console.log(error))
    }

    return (
        <div>
            {props.student ? (
                <div className  = "mb-3">

                <label htmlFor = "name" className = "form-label">Name</label>
                <input type ="text" className = "form-control"
                value = {name}
                placeholder = "Please enter Name"
                onChange = {(e) => setName(e.target.value)}
                />

                <label htmlFor = "id" className = "form-label">ID</label>
                <input type ="text" className = "form-control"
                value = {id}
                placeholder = "Please enter ID"
                onChange = {(e) => setId(e.target.value)}
                />

                <label htmlFor = "points" className = "form-label">Points</label>
                <input type ="text" className = "form-control"
                value = {points}
                placeholder = "Please enter Points"
                onChange = {(e) => setPoints(e.target.value)}
                />

                {
                    props.student.data_id ? <button
                    onClick = {updateStudent}
                    className = "btn btn-success mt-3"
                    >Update</button>
                    :
                    <button
                    onClick = {insertStudent}
                    className = "btn btn-primary mt-3"
                    >Insert</button>
                }  

                

                </div>    
            ):null}

        </div>
    )
}

export default Form

