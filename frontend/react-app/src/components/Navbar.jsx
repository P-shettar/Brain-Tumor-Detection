import React from 'react';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="nav-logo">
          <h2>🧠 Brain Tumor Detection</h2>
        </div>
        <div className="nav-links">
          <a href="#upload">Upload MRI</a>
          <a href="#about">About</a>
          <a href="#help">Help</a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;