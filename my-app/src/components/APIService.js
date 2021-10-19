

export default class APIService{
    static UpdateStudent(data_id, body){
        return fetch(`http://127.0.0.1:5000/update/${data_id}/`, {
            'method':'PUT',
            headers: {
              'Content-Type':'application/json'
            },
            body: JSON.stringify(body)
          })
          .then(resp => resp.json())
    }

    static InsertStudent(body){
      return fetch(`http://127.0.0.1:5000/create`, {
          'method':'POST',
          headers: {
            'Content-Type':'application/json'
          },
          body: JSON.stringify(body)
        })
        .then(resp => resp.json())
    }

    static DeleteStudent(data_id){
      return fetch(`http://127.0.0.1:5000/delete/${data_id}/`, {
          'method':'DELETE',
          headers: {
            'Content-Type':'application/json'
          },
        })
    }
}