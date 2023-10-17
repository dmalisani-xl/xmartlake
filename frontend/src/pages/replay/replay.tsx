import React from 'react';
import styles from './replay.module.scss';
import InteractiveGrid from './components/interactive-grid';
import gameData from './game-data';

const Replay = () => {
  return (
    <div className={styles.container}>
      <h1>Replay 🔁</h1>
      <InteractiveGrid gameData={gameData}/>
    </div>
  )
};

export { Replay };
