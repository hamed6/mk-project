import React, {Component} from 'react'
import { ReactDOM } from 'react'
import './ShipDetails.css'
import 'axios'
import axios from 'axios'


class GeneralView extends React.Component{
    constructor(props){
        super(props);
        this.state={
            shipResponse:[1,2,3],
        }
    };

    componentDidMount(){
        axios.get('http://127.0.0.1:8000/search')
        .then((response)=>
            this.setState=({shipResponse: response.data})
        )
    };

    render(){
        return(
            <div className="container">
            <div className="row align-items-start">
                <div className="col">
                    
                        <div>
                            <label>
                                Ship IMO
                            </label>
                            <select name='IMO'>
                                <option>From db</option>
                            </select>
                        </div>

                        <div>
                            <label>
                                Ship Name
                            </label>
                            <select name='Ship name'>
                                <option>From db</option>
                            </select>
                        </div>

                        <div>
                            <button>Get Ship</button>
                        </div>
                    
                    <div>
                        <label>
                            Date From:
                        </label>
                        <input type="date"></input>
                        <label>To:</label>
                        <input type="date"></input>
                    </div>

                    <div>
                        <label>
                            Log category
                        </label>
                        <select name='Log category'>
                            <option>From db</option>
                        </select>
                    </div>

                    <div>
                    <label>
                        Scenario query
                    </label>
                    <select name='Scenario'>
                        <option>From db</option>
                    </select>
                    </div>

                </div>                    
            </div>
            <div className="row align-items-end">
                <div className="col">
                    <p>
                        Placeholder for the chart
                    </p>

                    
                    
                 </div>
            </div>
            
            <div>
                {this.state.shipResponse.map((res)=>(
                        <p>{res}</p>
                    ))
                    }
            </div>
        </div>
        )
    }
}

export default GeneralView;