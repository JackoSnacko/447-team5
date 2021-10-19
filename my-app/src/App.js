import './App.css';
import {useState, useEffect} from 'react';
import StudentList from './components/StudentList';
import Form from './components/Form';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'

function App() {

  const [students, setStudents] = useState([]);
  const [editedStudent, setEditedStudent] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/read', {
      'method':'GET',
      headers: {
        'Content-Type':'application/json'
      }
    })
    .then(resp => resp.json())
    .then(resp => setStudents(resp))
    .catch(error => console.log(error))
  },[])

  const editStudent = (student) => {

    setEditedStudent(student)
  }

  const updatedData = (student) => {
    const new_student = students.map(my_student => {
      if(my_student.data_id === student.data_id){
        return student
      } else {
        return my_student
      }
    })
    setStudents(new_student)
  }

  const openForm = () => {
    setEditedStudent({name:'', id: '', points: ''})
  }

  const insertedStudent = (student) => {
    const new_students = [...students, student]
    setStudents(new_students)
  }

  const deleteStudent = (student) => {
    const new_students = students.filter(mystudent => {
      if(mystudent.data_id === student.data_id){
        return false
      }
      return true
    })
    setStudents(new_students)
  }

  return (
    
    <div className="App">
      <h1>Students:</h1>
      
      <StudentList students = {students} editStudent = {editStudent} deleteStudent = {deleteStudent}/>
      {editedStudent ? <Form student = {editedStudent} updatedData = {updatedData} insertedStudent = {insertedStudent}/> : null}
      

      <div className = "row">
        <div className = "col">
        </div>
        <div className = "col">
        <button
        className = "btn btn-primary"
        onClick = {openForm}
        >Insert Data</button>
        </div>
      </div>
      
      <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={false}>
        <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={[51.505, -0.09]}>
          <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
          </Popup>
        </Marker>
      </MapContainer>

    </div>
  );
}

export default App;
