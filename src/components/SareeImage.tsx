import React, { useState } from 'react';
import { Sparkles, ShoppingBag } from 'lucide-react';

interface SareeImageProps {
  src?: string;
  alt: string;
  className?: string;
  dominantColors?: string[];
  fabric?: string;
  primaryColor?: string;
}

export const SareeImage: React.FC<SareeImageProps> = ({
  src,
  alt,
  className = 'w-full h-full object-cover',
  dominantColors = ['#8B0000', '#B8860B', '#DC143C'],
  fabric = 'Silk',
  primaryColor = 'Catalog Saree',
}) => {
  const [hasError, setHasError] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const c1 = dominantColors[0] || '#4f46e5';
  const c2 = dominantColors[1] || '#9333ea';
  const c3 = dominantColors[2] || '#ca8a04';

  if (!src || hasError) {
    return (
      <div
        className={`w-full h-full flex flex-col items-center justify-center relative overflow-hidden p-4 select-none ${className}`}
        style={{
          background: `linear-gradient(135deg, ${c1}ee 0%, ${c2}dd 50%, ${c3}cc 100%)`,
        }}
      >
        {/* Subtle patterned overlay simulating saree weave */}
        <div
          className="absolute inset-0 opacity-15"
          style={{
            backgroundImage: `radial-gradient(circle at 50% 50%, #ffffff 1px, transparent 1px), radial-gradient(circle at 0% 0%, #ffffff 1px, transparent 1px)`,
            backgroundSize: '12px 12px',
          }}
        />

        <div className="z-10 flex flex-col items-center text-center text-white drop-shadow-md">
          <div className="w-10 h-10 rounded-full bg-white/20 backdrop-blur-xs flex items-center justify-center mb-2 border border-white/30 shadow-xs">
            <ShoppingBag className="w-5 h-5 text-white" />
          </div>
          <span className="text-xs font-bold leading-tight line-clamp-2 px-1 text-white">
            {primaryColor}
          </span>
          <span className="text-[10px] text-white/80 uppercase tracking-wider mt-0.5">
            {fabric}
          </span>
        </div>

        {/* Decorative Golden / Zari border simulator at bottom */}
        <div
          className="absolute bottom-0 inset-x-0 h-3"
          style={{
            background: `repeating-linear-gradient(45deg, #FFD700, #FFD700 4px, #B8860B 4px, #B8860B 8px)`,
            opacity: 0.85,
          }}
        />
      </div>
    );
  }

  return (
    <div className="w-full h-full relative overflow-hidden bg-gray-100 flex items-center justify-center">
      {isLoading && (
        <div
          className="absolute inset-0 animate-pulse flex items-center justify-center"
          style={{
            background: `linear-gradient(135deg, ${c1}33 0%, ${c2}22 100%)`,
          }}
        >
          <Sparkles className="w-4 h-4 text-gray-400 animate-spin" />
        </div>
      )}
      <img
        src={src}
        alt={alt}
        referrerPolicy="no-referrer"
        crossOrigin="anonymous"
        onLoad={() => setIsLoading(false)}
        onError={() => {
          setIsLoading(false);
          setHasError(true);
        }}
        className={`${className} ${isLoading ? 'opacity-0' : 'opacity-100'} transition-opacity duration-200`}
      />
    </div>
  );
};
