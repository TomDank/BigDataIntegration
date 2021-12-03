// this code creates the frontend search interface that reurn user queries

import React from 'react';
import './App.css';

class App  extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: [],
      value: ''
    };
    this.handleChange = this.handleChange.bind(this)
  }
  // user queries are formated and searched against the "Name" for keyword matching
  lookup() {
    fetch("/solr/kick/select?q=Name:" + "*" + this.state.value + "*")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result.response.docs
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }
  
  handleChange(event) {
    this.setState({value: event.target.value});
    this.lookup();
  }


  render() {
    return (
      <div className="App">
        <form onSubmit={this.handleSubmit}>
        <label>
          Keyword:
          <input type="text" value={this.state.value} onChange={this.handleChange} />
        </label>
        <input type="submit" value="Submit" />
      </form> 
      
          {this.state.items.map(item => (  
            // the list shows the fields that the search results will show on the frontend search interface
            <ul>
              <li > 
                {item.Name}<br/><br/>  
                {item.Description}<br/><br/>
                {item.Project_Summary}
                {item.Location}<br/><br/>
                {item.Name_of_Creator}<br/><br/>
                {item.CreatorName}<br/><br/>
                {item.Project_link}<br/><br/>
                {item.Project_Location}<br/><br/>
                {item.Project_Link}<br/><br/>
                {item.Creator_Urls}<br/><br/>
                {item.Campaign}<br/><br/>
                {item.story}<br/><br/>
                {item.ns}
                
                 
              </li>
            </ul>
          ))}
      </div>
    );
  }
}

export default App;
