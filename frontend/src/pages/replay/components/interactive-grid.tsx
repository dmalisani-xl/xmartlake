import React, { useEffect, useRef, useState } from 'react';
import { 
  getStartingPositions, createGrid, 
  drawStartingPositions, moveBot, 
  checkIfCirclesHaveBeenDrawn,
  colors, drawTurn
} from '../helpers';
import styles from './interactive-grid.module.scss';
import { createAvatar } from '@dicebear/core';
import { bottts } from '@dicebear/collection';
import heart from '../../../assets/icons/heart-icon.svg'
import drop from '../../../assets/icons/drop-icon.svg'
import bullets from '../../../assets/icons/rifle-gun-bullet-icon.svg'

interface InteractiveGridProps {
  gameData: GameData;
}

export interface BotData {
  id: string;
  name: string;
  color: string;
  avatar?: string;
  customAvatar?: string;
  turnInfo?: string;
  health: number;
  fuel: number;
  bullets: number;
}

export interface TurnInfo {
  message: string;
  health: number;
  fuel: number;
  bullets: number;
}

export interface BotTurnInfo {
  [botId: string]: TurnInfo;
}

export interface TurnLog {
  turnNumber: number;
  botData: BotData;
}

const NUM_ROWS = 50;
const NUM_COLS = 50;
const SQUARE_SIZE = 30;

const InteractiveGrid: React.FC<InteractiveGridProps> = ({ gameData }) => {
  const [currentTurn, setCurrentTurn] = useState<number>(0);
  const [botsData, setBotsData] = useState<BotData[]>([]);
  const [botTurnInfo, setBotTurnInfo] = useState<BotTurnInfo>({});
  const [turnLogs, setTurnLogs] = useState<TurnLog[]>([]);
  const [pause, setPause] = useState<boolean>(false);
  const gridRef = useRef<SVGSVGElement>(null);
  const assignColorsToBots = () => {
    const botsData: BotData[] = [];
    let i = 0;
    gameData.players.forEach((player) => {
      let avatar;
      let customAvatar;
      if (!player.avatar_b64) {
        avatar = createAvatar(bottts, {
          seed: player.bot_identifier,
          baseColor: [colors[i].hex.replace('#', '')],
        }).toDataUriSync();
      } else {
        customAvatar = player.avatar_b64;
      }
      const botData: BotData = {
        id: player.bot_identifier,
        name: player.name,
        color: colors[i].hex,
        avatar,
        customAvatar,
        health: player.health,
        fuel: player.fuel,
        bullets: player.bullets,
      };
      botsData.push(botData);
      i++;
    });

    setBotsData(botsData);
    return botsData;
  };

  useEffect(() => {
    const grid = gridRef.current;
    if (grid && !grid.hasChildNodes()) {
      createGrid(grid, NUM_ROWS, NUM_COLS, SQUARE_SIZE);
    }
  }, [gridRef.current]);

  useEffect(() => {
    const grid = gridRef.current;
    if (grid && currentTurn === 0) {
      const drawn = checkIfCirclesHaveBeenDrawn(grid);
      if (!drawn) {
        const startingPositions = getStartingPositions(gameData.players);
        const data = assignColorsToBots();
        drawStartingPositions(grid, startingPositions, SQUARE_SIZE, data);
      }
    }
    
  },[gridRef, gameData, currentTurn, botsData]);

  const handleNextTurn = () => {
    if (currentTurn < gameData.turns.length) {
      setCurrentTurn(currentTurn + 1);
      if(gridRef.current) {
        drawTurn(
          gridRef.current, gameData, currentTurn + 1,
          SQUARE_SIZE, botsData, setBotTurnInfo, setTurnLogs
        );
      }
    }
  };

  const handleAutoPlay = () => {
    for (let turn = 0; turn < gameData.turns.length && !pause; turn++) {
      setTimeout(() => {
        setCurrentTurn(turn + 1);
        if(gridRef.current) {
          drawTurn(
            gridRef.current, gameData, turn + 1,
            SQUARE_SIZE, botsData, setBotTurnInfo, setTurnLogs
          );
        }
      }, 1000 * turn);
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.grid}>
        <svg id="grid" width="750" height="750" ref={gridRef} />
        <button onClick={handleAutoPlay} disabled={currentTurn === gameData.turns.length}>
          Play ▶️
        </button>
        <div className={styles.logs}>
          <h2>Logs</h2>
          <div className={styles.logsContainer}>
            {turnLogs.map((turnLog) => (
              <div key={turnLog.turnNumber} className={styles.log}>
                <svg height="50" width="50">
                  <circle cx="25" cy="25" r="10" fill={turnLog.botData.color} />
                </svg>
                <p>Turn {turnLog.turnNumber}</p>
                <p>{turnLog.botData.turnInfo}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className={styles.bots}>
        {botsData.map((botData) => (
          <div key={botData.id}>
            <div className={styles.botsRef}>
              {botData.customAvatar && (
                <img src={`data:image/png;base64,${botData.customAvatar}`} width="40px" height="40px" id="bot-avatar" />
              )}
              {!botData.customAvatar && (
                <img src={botData.avatar} width="40px" height="40px" id="bot-avatar" />
              )}
              {botData.name}
              <svg height="24" width="24">
                <circle cx="12" cy="12" r="10" fill={botData.color} />
              </svg>
              <div className={styles.stats}>
                <div className={styles.stat}>
                  <img src={heart} width={25} height={25} />
                  { botTurnInfo[botData.id] ? botTurnInfo[botData.id].health : botData.health }
                </div>
                <div className={styles.stat}>
                  <img src={drop} width={25} height={25} />
                  { botTurnInfo[botData.id] ? botTurnInfo[botData.id].fuel : botData.fuel }
                </div>
                <div className={styles.stat}>
                  <img src={bullets} width={25} height={25} />
                  { botTurnInfo[botData.id] ? botTurnInfo[botData.id].bullets : botData.bullets }
                </div>
              </div>
              { botTurnInfo[botData.id] && botTurnInfo[botData.id].message }
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default InteractiveGrid;
