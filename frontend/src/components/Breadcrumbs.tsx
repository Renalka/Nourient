"use client";
import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Breadcrumbs() {
  const pathname = usePathname();
  if (!pathname || pathname === '/') return null;

  const segments = pathname.split('/').filter(p => p);
  
  // Build logical trail
  const trail = [{ name: 'Home', href: '/' }];
  
  // Add the actual current path segments
  segments.forEach((seg, idx) => {
    const name = seg.charAt(0).toUpperCase() + seg.slice(1);
    const href = `/${segments.slice(0, idx + 1).join('/')}`;
    trail.push({ name, href });
  });

  return (
    <nav className="flex text-xs text-gray-500 font-medium mb-4">
      {trail.map((item, idx) => {
        const isLast = idx === trail.length - 1;
        
        return (
          <div key={item.name} className="flex items-center">
            {idx > 0 && <span className="mx-2 text-gray-300">/</span>}
            {isLast ? (
              <span className="text-brand font-bold">{item.name}</span>
            ) : (
              <Link href={item.href} className="hover:text-brand transition-colors">{item.name}</Link>
            )}
          </div>
        );
      })}
    </nav>
  );
}
