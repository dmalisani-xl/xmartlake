import { Dispatch, SetStateAction } from "react";
import { BotData, BotTurnInfo, TurnLog } from "./components/interactive-grid";

export const colors: { name: string; hex: string }[] = [
  { name: 'Red', hex: '#FF0000' },
  { name: 'Green', hex: '#00FF00' },
  { name: 'Blue', hex: '#0000FF' },
  { name: 'Yellow', hex: '#FFFF00' },
  { name: 'Magenta', hex: '#FF00FF' },
  { name: 'Cyan', hex: '#00FFFF' },
  { name: 'Black', hex: '#000000' },
  { name: 'White', hex: '#FFFFFF' },
  { name: 'Orange', hex: '#FFA500' },
  { name: 'Purple', hex: '#800080' },
  { name: 'Dark Green', hex: '#008000' },
  { name: 'Teal', hex: '#008080' },
  { name: 'Maroon', hex: '#800000' },
  { name: 'Pink', hex: '#FFC0CB' },
  { name: 'Gold', hex: '#FFD700' },
  { name: 'Khaki', hex: '#F0E68C' },
  { name: 'Blue Violet', hex: '#8A2BE2' },
  { name: 'Indigo', hex: '#4B0082' },
  { name: 'Tomato', hex: '#FF6347' },
  { name: 'Spring Green', hex: '#00FF7F' },
  { name: 'Green Yellow', hex: '#ADFF2F' },
  { name: 'Dark Red', hex: '#8B0000' },
  { name: 'Chartreuse', hex: '#7FFF00' },
  { name: 'Slate Blue', hex: '#6A5ACD' },
  { name: 'Orange Red', hex: '#FF4500' },
  { name: 'Lime Green', hex: '#32CD32' },
  { name: 'Dark Orchid', hex: '#9932CC' },
  { name: 'Hot Pink', hex: '#FF69B4' },
  { name: 'Light Sea Green', hex: '#20B2AA' },
  { name: 'Chocolate', hex: '#D2691E' },
  { name: 'Lawn Green', hex: '#7CFC00' },
  { name: 'Medium Orchid', hex: '#BA55D3' },
  { name: 'Medium Sea Green', hex: '#3CB371' },
  { name: 'Medium Aquamarine', hex: '#66CDAA' },
  { name: 'Medium Slate Blue', hex: '#7B68EE' },
  { name: 'Medium Purple', hex: '#9370DB' },
  { name: 'Medium Turquoise', hex: '#48D1CC' },
  { name: 'Dark Sea Green', hex: '#8FBC8F' },
  { name: 'Light Salmon', hex: '#FFA07A' },
  { name: 'Rosy Brown', hex: '#BC8F8F' },
  { name: 'Sienna', hex: '#A0522D' },
  { name: 'Dark Orange', hex: '#FF8C00' },
  { name: 'Dark Turquoise', hex: '#00CED1' },
  { name: 'Dark Khaki', hex: '#BDB76B' },
  { name: 'Green Yellow', hex: '#ADFF2F' },
  { name: 'Purple', hex: '#800080' },
  { name: 'Olive Drab', hex: '#6B8E23' },
  { name: 'Salmon', hex: '#FA8072' },
  { name: 'Light Sea Green', hex: '#20B2AA' },
  { name: 'Light Slate Gray', hex: '#778899' },
  { name: 'Indian Red', hex: '#CD5C5C' },
  { name: 'Steel Blue', hex: '#4682B4' },
  { name: 'Sea Green', hex: '#2E8B57' },
  { name: 'Green Yellow', hex: '#ADFF2F' },
  { name: 'Brown', hex: '#A52A2A' },
  { name: 'Light Cyan', hex: '#E0FFFF' },
  { name: 'Spring Green', hex: '#00FF7F' },
  { name: 'Hot Pink', hex: '#FF69B4' },
  { name: 'Medium Sea Green', hex: '#3CB371' },
  { name: 'Maroon', hex: '#800000' },
  { name: 'Navy', hex: '#000080' },
  { name: 'Lime', hex: '#00FF00' },
  { name: 'Goldenrod', hex: '#DAA520' },
  { name: 'Gray', hex: '#808080' },
  { name: 'Dark Green', hex: '#008000' },
  { name: 'Saddle Brown', hex: '#8B4513' },
  { name: 'Chocolate', hex: '#D2691E' },
  { name: 'Indigo', hex: '#4B0082' },
  { name: 'Green Yellow', hex: '#ADFF2F' },
  { name: 'Dark Slate Gray', hex: '#2F4F4F' },
  { name: 'Orange Red', hex: '#FF4500' },
  { name: 'Slate Blue', hex: '#6A5ACD' },
  { name: 'Dark Orchid', hex: '#9932CC' },
  { name: 'Sienna', hex: '#A0522D' },
  { name: 'Lime Green', hex: '#32CD32' },
  { name: 'Medium Slate Blue', hex: '#7B68EE' },
  { name: 'Medium Turquoise', hex: '#48D1CC' },
  { name: 'Purple', hex: '#800080' },
  { name: 'Medium Aquamarine', hex: '#66CDAA' },
  { name: 'Gold', hex: '#FFD700' },
  { name: 'Blue Violet', hex: '#8A2BE2' },
  { name: 'Green Yellow', hex: '#ADFF2F' },
  { name: 'Peru', hex: '#CD853F' },
  { name: 'Medium Blue', hex: '#0000CD' },
  { name: 'Dark Violet', hex: '#9400D3' },
  { name: 'Medium Spring Green', hex: '#00FA9A' },
  { name: 'Dim Gray', hex: '#696969' },
  { name: 'Light Sea Green', hex: '#20B2AA' },
  { name: 'Dark Sea Green', hex: '#8FBC8F' },
  { name: 'Purple', hex: '#800080' },
  { name: 'Orange Red', hex: '#FF4500' },
  { name: 'Medium Purple', hex: '#9370DB' },
  { name: 'Sienna', hex: '#A0522D' },
  { name: 'Green Yellow', hex: '#ADFF2F' },
  { name: 'Olive Drab', hex: '#6B8E23' },
  { name: 'Medium Turquoise', hex: '#48D1CC' },
  { name: 'Indian Red', hex: '#CD5C5C' },
  { name: 'Purple', hex: '#800080' },
  { name: 'Chocolate', hex: '#D2691E' },
  { name: 'Dark Slate Gray', hex: '#2F4F4F' }
];

const buildMovementAnimationKeyframes = (
  botIdentifier: string, name: string, x: number | string, y: number | string, 
  newX: number | string, newY: number | string
  ) => {
  const animationName = `${name}_${botIdentifier}`;
  const animationKeyframes = `
    @keyframes ${animationName} {
      from {
          cx: ${x};
          cy: ${y};
      }
      to {
          cx: ${newX};
          cy: ${newY};
      }
    }
  `;
  return {animationName, animationKeyframes};
}

const buildShakeAnimationKeyframes = (botIdentifier: string, name: string) => {
  const animationName = `${name}_${botIdentifier}`;
  const animationKeyframes = `
    @keyframes ${animationName} {
      0% {
        transform: translate(0, 0);
      }
      10% {
        transform: translate(-5px, 0);
      }
      20% {
        transform: translate(5px, 0);
      }
      30% {
        transform: translate(-5px, 0);
      }
      40% {
        transform: translate(5px, 0);
      }
      50% {
        transform: translate(-5px, 0);
      }
      60% {
        transform: translate(5px, 0);
      }
      70% {
        transform: translate(-5px, 0);
      }
      80% {
        transform: translate(5px, 0);
      }
      90% {
        transform: translate(-5px, 0);
      }
      100% {
        transform: translate(0, 0);
      }
    }
  `;
  return { animationName, animationKeyframes };
}

const buildPulseAnimationKeyframes = (botIdentifier: string, name: string, from: string, to: string) => {
  const animationName = `${name}_${botIdentifier}`;
  const animationKeyframes = `
    @keyframes ${animationName} {
      from {
        r: ${from};
      }
      to {
        r: ${to};
      }
    }
  `;
  return { animationName, animationKeyframes };
}

const appendStyleElement = (
  grid: SVGSVGElement, element: SVGCircleElement, 
  animation: { animationName: string, animationKeyframes: string }, 
  withTimeOut: boolean, svgNS: string, animationType: string = "linear",
  animationDuration: string = "1s", animationFillMode: string = "forwards"
  ) => {
  const styleElement = document.createElementNS(svgNS, "style");
  styleElement.innerHTML = animation.animationKeyframes;
  grid.appendChild(styleElement);
  if (withTimeOut) {
    setTimeout(() => {
      element.style.animation = `${animation.animationName} ${animationDuration} ${animationType} ${animationFillMode}`;
    }, 500)
  } else {
    element.style.animation = `${animation.animationName} ${animationDuration} ${animationType} ${animationFillMode}`;
  }
}

export const getStartingPositions = (palyers: PlayerData[]) => {
  const startingPositions = palyers
    .map((player) => {
      return {
          botIdentifier: player.bot_identifier,
          x: player.position_x,
          y: player.position_y,
      };
    }
  );
  return startingPositions;
}

export const createGrid = (grid: SVGSVGElement, rows: number, cols: number, squareSize: number) => {
    const svgNS = "http://www.w3.org/2000/svg";
    const gridGroup = document.createElementNS(svgNS, "g");

    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        const rect = document.createElementNS(svgNS, "rect");
        rect.setAttribute("x", (j * squareSize).toString());
        rect.setAttribute("y", (i * squareSize).toString());
        rect.setAttribute("width", squareSize.toString());
        rect.setAttribute("height", squareSize.toString());
        rect.setAttribute("fill", "none");
        rect.setAttribute("stroke", "black");
        gridGroup.appendChild(rect);
      }
    }

    const viewBoxWidth = cols * squareSize;
    const viewBoxHeight = rows * squareSize;
    grid.setAttribute("viewBox", `0 0 ${viewBoxWidth} ${viewBoxHeight}`);
    grid.appendChild(gridGroup);
};

export const drawStartingPositions = (grid: SVGSVGElement, startingPositions: any[], squareSize: number, botsData: any[]) => {
  const svgNS = "http://www.w3.org/2000/svg";
  startingPositions.forEach((position) => {
    const circle = document.createElementNS(svgNS, "circle");

    const centerX = position.x * squareSize + squareSize / 2;
    const centerY = position.y * squareSize + squareSize / 2;

    const color = botsData.find((bot) => bot.id === position.botIdentifier)?.color;

    circle.setAttribute("cx", centerX.toString());
    circle.setAttribute("cy", centerY.toString());
    circle.setAttribute("r", "10");
    circle.setAttribute("fill", color);
    circle.setAttribute("id", position.botIdentifier);
    grid.appendChild(circle);
  });
};

export const moveBot = (
  grid: SVGSVGElement, botIdentifier: 
  string,x: number, y: number, newX: number, newY: 
  number, squareSize: number, color: string, collision: boolean,
  collision_to: string, origin_shield_enabled: boolean, 
  origin_victories: number, final_victories: number, dead: boolean
  ) => {
  const svgNS = "http://www.w3.org/2000/svg";

  const existingBotCircle = document.querySelector(`#${botIdentifier}`) as SVGCircleElement;
  if (existingBotCircle) {
    existingBotCircle.remove();
  }

  const newCenterX = newX * squareSize + squareSize / 2;
  const newCenterY = newY * squareSize + squareSize / 2;

  const newBotCircle = document.createElementNS(svgNS, "circle");
  newBotCircle.setAttribute("id", botIdentifier);
  newBotCircle.setAttribute("cx", newCenterX.toString());
  newBotCircle.setAttribute("cy", newCenterY.toString());
  newBotCircle.setAttribute("r", "10");
  newBotCircle.setAttribute("fill", origin_shield_enabled ? "none" : color);
  grid.appendChild(newBotCircle);

  if (collision) {
    const collidedBotCircle = document.querySelector(`#${collision_to}`) as SVGCircleElement;
    const collidedBotCircleCenterX = collidedBotCircle.getAttribute("cx");
    const collidedBotCircleCenterY = collidedBotCircle.getAttribute("cy");

    const collisionAnimation = buildMovementAnimationKeyframes(botIdentifier, "collisionAnimation", x * squareSize + squareSize / 2, y * squareSize + squareSize / 2, collidedBotCircleCenterX!, collidedBotCircleCenterY!);
    const shakeAnimation = buildShakeAnimationKeyframes(collision_to, "shakeAnimation");
    const moveToFinalPositionAnimation = buildMovementAnimationKeyframes(botIdentifier, "moveToFinalPositionAnimation", collidedBotCircleCenterX!, collidedBotCircleCenterY!, newCenterX, newCenterY);

    appendStyleElement(grid, newBotCircle, collisionAnimation, false, svgNS, "ease-in", "0.5s", "forwards");
    appendStyleElement(grid, collidedBotCircle, shakeAnimation, true, svgNS);
    appendStyleElement(grid, newBotCircle, moveToFinalPositionAnimation, true, svgNS);

    if (final_victories > origin_victories) {
      collidedBotCircle.remove();
    }

    if (dead) {
      newBotCircle.remove();
    }

  } else {
    const moveBotAnimation = buildMovementAnimationKeyframes(botIdentifier, "moveBotAnimation", x * squareSize + squareSize / 2, y * squareSize + squareSize / 2, newCenterX, newCenterY);
    appendStyleElement(grid, newBotCircle, moveBotAnimation, false, svgNS);
  }
};

const drawShield = (grid: SVGSVGElement, botIdentifier: string, color: string, final_shield_enabled: boolean) => {
  const svgNS = "http://www.w3.org/2000/svg";

  const existingBotCircle = document.querySelector(`#${botIdentifier}`) as SVGCircleElement;
  if (existingBotCircle) {
    existingBotCircle.remove();
  }

  const newShieldCircle = document.createElementNS(svgNS, "circle");
  newShieldCircle.setAttribute("id", botIdentifier);
  newShieldCircle.setAttribute("cx", existingBotCircle.getAttribute("cx") || "0");
  newShieldCircle.setAttribute("cy", existingBotCircle.getAttribute("cy") || "0");
  newShieldCircle.setAttribute("r", "10");
  newShieldCircle.setAttribute("fill", final_shield_enabled ? "none" : color);
  final_shield_enabled && newShieldCircle.setAttribute("stroke", color);
  newShieldCircle.setAttribute("stroke-width", "5");
  grid.appendChild(newShieldCircle);
}

const pulse = (grid: SVGSVGElement, botIdentifier: string, color: string, origin_shield_enabled: boolean) => {
  const svgNS = "http://www.w3.org/2000/svg";

  const existingBotCircle = document.querySelector(`#${botIdentifier}`) as SVGCircleElement;
  if (existingBotCircle) {
    existingBotCircle.remove();
  }

  const newRefuelCircle = document.createElementNS(svgNS, "circle");
  newRefuelCircle.setAttribute("id", botIdentifier);
  newRefuelCircle.setAttribute("cx", existingBotCircle.getAttribute("cx") || "0");
  newRefuelCircle.setAttribute("cy", existingBotCircle.getAttribute("cy") || "0");
  newRefuelCircle.setAttribute("r", "10");
  newRefuelCircle.setAttribute("fill", origin_shield_enabled ? "none" : color);
  grid.appendChild(newRefuelCircle);

  const firstAnimation = buildPulseAnimationKeyframes(botIdentifier, "refuelAnimationUp", "10", "15");
  const secondAnimation = buildPulseAnimationKeyframes(botIdentifier, "refuelAnimationDown", "15", "10");

  appendStyleElement(grid, newRefuelCircle, firstAnimation, false, svgNS, "linear", "0.5s", "forwards");
  appendStyleElement(grid, newRefuelCircle, secondAnimation, true, svgNS, "linear", "0.5s", "forwards");
}

const fire = (
  grid: SVGSVGElement, botIdentifier: string,
  hit: boolean, hit_to: string | null,
  target_abs_coordinates: string, squareSize: number, 
  origin_victories: number, final_victories: number,
  ) => {
  const svgNS = "http://www.w3.org/2000/svg";

  const existingBotCircle = document.querySelector(`#${botIdentifier}`) as SVGCircleElement;

  const fireCircle = document.createElementNS(svgNS, "circle");
  fireCircle.setAttribute("id", botIdentifier+"_bullet");
  fireCircle.setAttribute("cx", existingBotCircle.getAttribute("cx") || "0");
  fireCircle.setAttribute("cy", existingBotCircle.getAttribute("cy") || "0");
  fireCircle.setAttribute("r", "5");
  fireCircle.setAttribute("fill", "black");
  grid.appendChild(fireCircle);

  const targets = target_abs_coordinates.match(/\d+/g);
  const parsedTargets = targets?.map(Number);

  const fireAnimation = buildMovementAnimationKeyframes(
    botIdentifier, "fireAnimation", existingBotCircle.getAttribute("cx") || "0", 
    existingBotCircle.getAttribute("cy") || "0", parsedTargets![0] * squareSize + squareSize / 2, 
    parsedTargets![1] * squareSize + squareSize / 2
  );

  appendStyleElement(grid, fireCircle, fireAnimation, false, svgNS, "linear", "0.5s", "forwards");

  if (hit) {
    const target = (document.querySelector(`#${hit_to}`) as SVGCircleElement);
    const shakeAnimation = buildShakeAnimationKeyframes(hit_to!, "shakeAnimation");
    appendStyleElement(grid, target, shakeAnimation, true, svgNS);

    if (final_victories > origin_victories) {
      target.remove();
    }
  }
  
  setTimeout(() => {
    fireCircle.remove();
  }, 500);
}

export const checkIfCirclesHaveBeenDrawn = (grid: SVGSVGElement) => {
  const circles = grid.querySelectorAll("circle");
  return circles.length > 0;
};

const getCurrentTurn = (turnData: TurnData[], turnNumber: number) => {
  return turnData.filter((turn) => turn.turn_number === turnNumber);
};

export const drawTurn = (
  grid: SVGSVGElement, gameData: GameData, 
  turnNumber: number, squareSize: number, botsData: BotData[], 
  setBotTurnInfo: Dispatch<SetStateAction<BotTurnInfo>>, 
  setTurnLogs: Dispatch<SetStateAction<TurnLog[]>>
  ) => {
  const currentTurn = getCurrentTurn(gameData.turns, turnNumber);
  for (let i = 0; i < currentTurn.length; i++) {
    const turn = currentTurn[i];
    const bot = botsData.find((bot) => bot.id === turn.bot_identifier);
    if (bot) {
      const color = bot.color;
      const { 
        bot_identifier: botIdentifier, origin_position_x: x, 
        origin_position_y: y, final_position_x: newX, 
        final_position_y: newY, origin_shield_enabled, 
        final_shield_enabled, collision, collision_to,
        hit, hit_to, target_abs_coordinates, origin_victories,
        final_victories, dead, action, final_fuel, final_health,
        final_bullets
      } = turn;

      setTimeout(() => {
        switch (action) {
          case 'M':
            moveBot(
              grid, botIdentifier, x, y, newX, newY, 
              squareSize, color, collision, collision_to, 
              origin_shield_enabled, origin_victories,
              final_victories, dead
            );
            let moveMessage : string;
            if (collision) {
              const target = botsData.find((bot) => bot.id === turn.collision_to);
              moveMessage = "Moved to " + newX + ", " + newY + " and collided with " + target?.name;
              if (dead && final_victories > origin_victories) {
                moveMessage += " and both died";
              }
              if (dead && final_victories === origin_victories) {
                moveMessage += " and died";
              }
              if (!dead && final_victories > origin_victories) {
                moveMessage += `. ${target?.name} died`;
              }
            } else {
              moveMessage = "Moved to " + newX + ", " + newY;
            }
            setBotTurnInfo((prevState) => {
              return {
                ...prevState,
                [botIdentifier]: {
                  message: moveMessage,
                  health: final_health,
                  fuel: final_fuel > 0 ? final_fuel : 0,
                  bullets: final_bullets > 0 ? final_bullets : 0,
                }
              }
            });
            setTurnLogs((prevState) => {
              return [...prevState, {
                turnNumber,
                botData: {
                  id: botIdentifier,
                  name: bot.name,
                  color,
                  turnInfo: moveMessage,
                  avatar: bot.avatar,
                  health: final_health > 0 ? final_health : 0,
                  fuel: final_fuel > 0 ? final_fuel : 0,
                  bullets: final_bullets > 0 ? final_bullets : 0,
                }
              }]
            });
          break;
          case 'S':
            drawShield(grid, botIdentifier, color, final_shield_enabled);
            let shieldMessage: string;
            if (final_shield_enabled) {
              shieldMessage = "Shielded";
            } else {
              shieldMessage = "Unshielded";
            }
            setBotTurnInfo((prevState) => {
              return {
                ...prevState,
                [botIdentifier]: {
                  message: shieldMessage,
                  health: final_health > 0 ? final_health : 0,
                  fuel: final_fuel > 0 ? final_fuel : 0,
                  bullets: final_bullets > 0 ? final_bullets : 0,
                }
              }
            });
            setTurnLogs((prevState) => {
              return [...prevState, {
                turnNumber,
                botData: {
                  id: botIdentifier,
                  name: bot.name,
                  color,
                  turnInfo: shieldMessage,
                  avatar: bot.avatar,
                  health: final_health > 0 ? final_health : 0,
                  fuel: final_fuel > 0 ? final_fuel : 0,
                  bullets: final_bullets > 0 ? final_bullets : 0,
                }
              }]
            });
          break;
          case 'R':
            pulse(grid, botIdentifier, color, origin_shield_enabled);
            setBotTurnInfo((prevState) => {
              return {
                ...prevState,
                [botIdentifier]: {
                  message: "Refueled",
                  health: final_health > 0 ? final_health : 0,
                  fuel: final_fuel > 0 ? final_fuel : 0,
                  bullets: final_bullets > 0 ? final_bullets : 0,
                }
              }
            });
            setTurnLogs((prevState) => {
              return [...prevState, {
                turnNumber,
                botData: {
                  id: botIdentifier,
                  name: bot.name,
                  color,
                  turnInfo: "Refueled",
                  avatar: bot.avatar,
                  health: final_health > 0 ? final_health : 0,
                  fuel: final_fuel > 0 ? final_fuel : 0,
                  bullets: final_bullets > 0 ? final_bullets : 0,
                }
              }]
            });
          break;
          case 'L':
            pulse(grid, botIdentifier, color, origin_shield_enabled);
            setBotTurnInfo((prevState) => {
              return {
                ...prevState,
                [botIdentifier]: {
                  message: "Reloaded",
                  health: final_health,
                  fuel: final_fuel > 0 ? final_fuel : 0,
                  bullets: final_bullets > 0 ? final_bullets : 0,
                }
              }
            });
            setTurnLogs((prevState) => {
              return [...prevState, {
                turnNumber,
                botData: {
                  id: botIdentifier,
                  name: bot.name,
                  color,
                  turnInfo: "Reloaded",
                  avatar: bot.avatar,
                  health: final_health > 0 ? final_health : 0,
                  fuel: final_fuel > 0 ? final_fuel : 0,
                  bullets: final_bullets > 0 ? final_bullets : 0,
                }
              }]
            });
          break;
          case 'F':
            fire(grid, botIdentifier, hit, hit_to, target_abs_coordinates, squareSize, origin_victories, final_victories);
            let fireMessage: string;
            if (hit) {
              const target = botsData.find((bot) => bot.id === turn.hit_to);
              fireMessage = "Fired at " + target?.name;
              if (final_victories > origin_victories) {
                fireMessage += " and killed them";
              }
            } else {
              fireMessage = "Fired";
            }
            setBotTurnInfo((prevState) => {
              return {
                ...prevState,
                [botIdentifier]: {
                  message: fireMessage,
                  health: final_health > 0 ? final_health : 0,
                  fuel: final_fuel > 0 ? final_fuel : 0,
                  bullets: final_bullets > 0 ? final_bullets : 0,
                }
              }
            });
            setTurnLogs((prevState) => {
              return [...prevState, {
                turnNumber,
                botData: {
                  id: botIdentifier,
                  name: bot.name,
                  color,
                  turnInfo: fireMessage,
                  avatar: bot.avatar,
                  health: final_health > 0 ? final_health : 0,
                  fuel: final_fuel > 0 ? final_fuel : 0,
                  bullets: final_bullets > 0 ? final_bullets : 0,
                }
              }]
            });
            break;
          case 'T':
            pulse(grid, botIdentifier, color, origin_shield_enabled);
              setBotTurnInfo((prevState) => {
                return {
                  ...prevState,
                  [botIdentifier]: {
                    message: "Repaired",
                    health: final_health > 0 ? final_health : 0,
                    fuel: final_fuel > 0 ? final_fuel : 0,
                    bullets: final_bullets > 0 ? final_bullets : 0,
                  }
                }
              });
              setTurnLogs((prevState) => {
                return [...prevState, {
                  turnNumber,
                  botData: {
                    id: botIdentifier,
                    name: bot.name,
                    color,
                    turnInfo: "Repaired",
                    avatar: bot.avatar,
                    health: final_health > 0 ? final_health : 0,
                    fuel: final_fuel > 0 ? final_fuel : 0,
                    bullets: final_bullets > 0 ? final_bullets : 0,
                  }
                }]
              });
          break;
          case '/':
            setBotTurnInfo((prevState) => {
              return {
                ...prevState,
                [botIdentifier]: {
                  message: "Skipped",
                  health: final_health > 0 ? final_health : 0,
                  fuel: final_fuel > 0 ? final_fuel : 0,
                  bullets: final_bullets > 0 ? final_bullets : 0,
                }
              }
            });
            setTurnLogs((prevState) => {
              return [...prevState, {
                turnNumber,
                botData: {
                  id: botIdentifier,
                  name: bot.name,
                  color,
                  turnInfo: "Skipped",
                  avatar: bot.avatar,
                  health: final_health > 0 ? final_health : 0,
                  fuel: final_fuel > 0 ? final_fuel : 0,
                  bullets: final_bullets > 0 ? final_bullets : 0,
                }
              }]
            });
          break;
        }
      }, 1000 * i);
    }
  }
};
