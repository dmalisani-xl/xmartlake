import React, { useState, useEffect } from 'react';
import TextEditor from './components/text-editor';
import styles from './home.module.scss';

const Home = () => {
  return (
    <div className={styles.container}>
      <h1>XmartLake 🤖</h1>
      <TextEditor />
    </div>
  )
};

export { Home };
