"""
Custom Stock Lists Import and Management for StockWise
Supports CSV/Excel file upload and processing for custom stock universes
"""

import os
import csv
import json
import uuid
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import pandas as pd
from io import StringIO, BytesIO
from fastapi import UploadFile, HTTPException

logger = logging.getLogger(__name__)

class CustomListManager:
    """Manager for custom stock lists - upload, validate, and store"""
    
    def __init__(self, upload_dir: str = "/app/uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        self.custom_lists = {}  # In-memory storage for now
    
    async def process_uploaded_file(self, file: UploadFile, list_name: str = None) -> Dict[str, Any]:
        """
        Process uploaded CSV/Excel file and extract stock symbols
        
        Args:
            file: Uploaded file (CSV or Excel)
            list_name: Custom name for the list
            
        Returns:
            Dictionary with processing results and extracted symbols
        """
        try:
            # Validate file
            if not file.filename:
                raise HTTPException(status_code=400, detail="No file provided")
            
            file_extension = Path(file.filename).suffix.lower()
            if file_extension not in ['.csv', '.xlsx', '.xls', '.txt']:
                raise HTTPException(
                    status_code=400, 
                    detail="Unsupported file format. Please upload CSV, Excel (.xlsx/.xls), or TXT files"
                )
            
            # Generate unique list ID
            list_id = str(uuid.uuid4())[:8]
            if not list_name:
                list_name = f"Custom_List_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Read file content
            content = await file.read()
            
            # Process based on file type
            if file_extension == '.csv' or file_extension == '.txt':
                symbols = await self._process_csv_content(content, file.filename)
            else:  # Excel files
                symbols = await self._process_excel_content(content, file.filename)
            
            # Validate symbols
            validated_symbols = self._validate_symbols(symbols)
            
            # Store the custom list
            custom_list = {
                'list_id': list_id,
                'name': list_name,
                'filename': file.filename,
                'symbols': validated_symbols['valid_symbols'],
                'invalid_symbols': validated_symbols['invalid_symbols'],
                'total_count': len(validated_symbols['valid_symbols']),
                'created_at': datetime.utcnow().isoformat(),
                'file_extension': file_extension
            }
            
            self.custom_lists[list_id] = custom_list
            
            logger.info(f"Processed custom list {list_id}: {len(validated_symbols['valid_symbols'])} valid symbols")
            
            return {
                'success': True,
                'list_id': list_id,
                'list_name': list_name,
                'symbols_count': len(validated_symbols['valid_symbols']),
                'invalid_count': len(validated_symbols['invalid_symbols']),
                'symbols_preview': validated_symbols['valid_symbols'][:20],  # First 20 symbols
                'invalid_symbols': validated_symbols['invalid_symbols'],
                'processing_summary': validated_symbols['summary']
            }
            
        except Exception as e:
            logger.error(f"Failed to process uploaded file {file.filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
    
    async def _process_csv_content(self, content: bytes, filename: str) -> List[str]:
        """Process CSV/TXT file content and extract symbols"""
        try:
            # Decode content
            text_content = content.decode('utf-8-sig')  # Handle BOM
            
            # Try different CSV parsing approaches
            symbols = []
            
            # Approach 1: Simple line-by-line (for TXT files or single-column CSV)
            lines = text_content.strip().split('\n')
            if len(lines) > 1 and ',' not in lines[0]:
                # Likely a TXT file with one symbol per line
                for line in lines:
                    symbol = line.strip().upper()
                    if symbol and self._is_potential_symbol(symbol):
                        symbols.append(symbol)
                return symbols
            
            # Approach 2: CSV with headers
            csv_reader = csv.DictReader(StringIO(text_content))
            
            # Look for symbol columns (common header names)
            symbol_columns = []
            if csv_reader.fieldnames:
                for field in csv_reader.fieldnames:
                    field_lower = field.lower().strip()
                    if any(keyword in field_lower for keyword in ['symbol', 'ticker', 'stock', 'code']):
                        symbol_columns.append(field)
            
            # Extract symbols from identified columns
            for row in csv_reader:
                for col in symbol_columns:
                    if col in row and row[col]:
                        symbol = str(row[col]).strip().upper()
                        if self._is_potential_symbol(symbol):
                            symbols.append(symbol)
            
            # Approach 3: First column if no headers found
            if not symbols and csv_reader.fieldnames:
                csv_reader = csv.reader(StringIO(text_content))
                for row in csv_reader:
                    if row and len(row) > 0:
                        symbol = str(row[0]).strip().upper()
                        if self._is_potential_symbol(symbol):
                            symbols.append(symbol)
            
            return list(set(symbols))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Failed to process CSV content from {filename}: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
    
    async def _process_excel_content(self, content: bytes, filename: str) -> List[str]:
        """Process Excel file content and extract symbols"""
        try:
            # Read Excel file
            df = pd.read_excel(BytesIO(content), sheet_name=0)  # First sheet
            
            symbols = []
            
            # Look for symbol columns
            symbol_columns = []
            for col in df.columns:
                col_lower = str(col).lower().strip()
                if any(keyword in col_lower for keyword in ['symbol', 'ticker', 'stock', 'code']):
                    symbol_columns.append(col)
            
            # Extract symbols from identified columns
            for col in symbol_columns:
                for value in df[col].dropna():
                    symbol = str(value).strip().upper()
                    if self._is_potential_symbol(symbol):
                        symbols.append(symbol)
            
            # If no symbol columns found, try first column
            if not symbols and len(df.columns) > 0:
                first_col = df.columns[0]
                for value in df[first_col].dropna():
                    symbol = str(value).strip().upper()
                    if self._is_potential_symbol(symbol):
                        symbols.append(symbol)
            
            return list(set(symbols))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Failed to process Excel content from {filename}: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid Excel format: {str(e)}")
    
    def _is_potential_symbol(self, symbol: str) -> bool:
        """Check if a string could be a valid stock symbol"""
        if not symbol or len(symbol) < 1 or len(symbol) > 10:
            return False
        
        # Basic validation - alphanumeric with possible dots/dashes
        if not symbol.replace('.', '').replace('-', '').isalnum():
            return False
        
        # Skip common non-symbol text
        skip_words = {
            'SYMBOL', 'TICKER', 'STOCK', 'CODE', 'NAME', 'COMPANY', 
            'PRICE', 'VOLUME', 'DATE', 'TIME', 'NULL', 'NA', 'N/A', ''
        }
        
        if symbol.upper() in skip_words:
            return False
        
        return True
    
    def _validate_symbols(self, symbols: List[str]) -> Dict[str, Any]:
        """Validate extracted symbols against common patterns"""
        valid_symbols = []
        invalid_symbols = []
        
        for symbol in symbols:
            # Additional validation rules
            if len(symbol) >= 1 and len(symbol) <= 6:  # Most US stocks are 1-6 characters
                if symbol.isalpha() or ('.' in symbol and symbol.count('.') == 1):
                    valid_symbols.append(symbol)
                else:
                    invalid_symbols.append(symbol)
            else:
                invalid_symbols.append(symbol)
        
        return {
            'valid_symbols': list(set(valid_symbols)),  # Remove duplicates
            'invalid_symbols': list(set(invalid_symbols)),
            'summary': {
                'total_extracted': len(symbols),
                'valid_count': len(set(valid_symbols)),
                'invalid_count': len(set(invalid_symbols)),
                'duplicate_removed': len(symbols) - len(set(symbols))
            }
        }
    
    def get_custom_list(self, list_id: str) -> Optional[Dict[str, Any]]:
        """Get custom list by ID"""
        return self.custom_lists.get(list_id)
    
    def get_all_custom_lists(self) -> List[Dict[str, Any]]:
        """Get all custom lists (summary info)"""
        return [
            {
                'list_id': list_data['list_id'],
                'name': list_data['name'],
                'symbols_count': list_data['total_count'],
                'created_at': list_data['created_at'],
                'filename': list_data['filename']
            }
            for list_data in self.custom_lists.values()
        ]
    
    def delete_custom_list(self, list_id: str) -> bool:
        """Delete a custom list"""
        if list_id in self.custom_lists:
            del self.custom_lists[list_id]
            logger.info(f"Deleted custom list {list_id}")
            return True
        return False
    
    def get_symbols_for_batch(self, list_id: str) -> List[str]:
        """Get symbols from custom list for batch processing"""
        custom_list = self.custom_lists.get(list_id)
        if custom_list:
            return custom_list['symbols']
        return []

# Global instance
custom_list_manager = CustomListManager()