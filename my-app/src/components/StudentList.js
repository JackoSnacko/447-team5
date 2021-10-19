import React from 'react'
import APIService from './APIService'

function StudentList(props) {

    const editStudent = (student) => {
        props.editStudent(student)
    }

    const deleteStudent = (student) => {
        APIService.DeleteStudent(student.data_id)
        .then(() => props.deleteStudent(student))
    }

    return (
        <div>
            {props.students && props.students.map(student => {
        return (
          <div key = {student.data_id}>
            <p>Name: {student.name}</p>
            <p>ID: {student.id}</p>
            <p>Points: {student.points}</p>


            <div className = "row">
                <div className = "col-md-1">
                    <button className = "btn btn-success"
                    onClick = {() => editStudent(student)}
                    >Update</button>
                </div>

                <div className = "col">
                    <button className = "btn btn-danger"
                    onClick = {() => deleteStudent(student)}
                    >Delete</button>
                </div>

            </div>

            <hr/>

          </div>
        )
      })}
        </div>
    )
}


export default StudentList


