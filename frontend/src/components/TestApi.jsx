import axios from 'axios';
import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import { setData } from '../redux/features/dataSlice';

const TestApi = () => {
    const dispatch = useDispatch();
    const data = useSelector((state) => state.data.value);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/hello/").then((response) => {
            dispatch(setData(response.data));
            console.log(response.data);
        });
    }, [dispatch]);

  return (
    <div>{data.message ? <p>{data.message}</p> : <p>No message found.</p>}</div>
  )
}

export default TestApi