// src/components/shared/DojoLogo.js
import React from 'react';

const DojoLogo = ({ size = 48, className = "" }) => {
  // Aumenta a altura em 20% para dar mais espaço vertical
  const adjustedHeight = Math.round(size * 1.2);

  return (
    <div className={`relative ${className}`} style={{ width: size, height: adjustedHeight }}>
      <img
        src="/logo-dojo-poker_final.png"
        alt="Dojo Poker Logo"
        width={size}
        height={adjustedHeight}
        className="drop-shadow-lg"
        style={{ width: size, height: adjustedHeight }}
      />
    </div>
  );
};

export default DojoLogo;
