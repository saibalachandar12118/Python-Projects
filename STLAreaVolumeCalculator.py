# Author : SAI BALACHANDAR V
import numpy as np
import math
class STLAreaVolumeCalculator: 
  '''
    ===============================================================================
    STL Area & Volume Calculator
    ===============================================================================
        Author  : SAI BALACHANDAR V
        A utility class to compute the total surface area and enclosed volume
        of an ASCII STL 3D model.
        Using Gauss Divergence Therem  : https://en.wikipedia.org/wiki/Divergence_theorem

        Usage Example
        -------------
        # >>> from stl_area_volume import STLAreaVolumeCalculator
        #>>> calc = STLAreaVolumeCalculator("path/to/model.stl")
        # >>> print(calc)
        STL File: path/to/model.stl
        Total Surface Area: 1234.567890 mm²
        Total Volume: 9876.543210 mm³
  
  '''

  def __init__(self,File_path,compute_on_init=True):       
      self.File_path = File_path       
      self._tria_facet_lst= []       
      self.total_area = 0       
      self.total_volume = 0       
      self._parser_stl()        
      if compute_on_init:           
          self.compute()     
  
  @property   
  def tria_facets_getter(self):   
     """Return the list of parsed triangular facets."""
     return self._tria_facet_lst   

  def _parser_stl(self):     
      # Parse STL file into facets       
      """       
       Internal method to parse an ASCII STL file.       
       Extracts normals and vertices for each facet and stores them       
       in self._facets as separate triangular facets.       
       """       
      p_list =[]       
      try:           
          with open(self.File_path,'r') as i_file:               
              for line in i_file.readlines():                   
                  line = line.strip()                   
                  if line.startswith("vertex") or line.startswith("facet"):                       
                      try :                           
                          coords = ([float(x) for x in (line.split()[-3:])])                       
                      except ValueError:                           
                          continue                       
                      p_list.append(coords)                   
                  if len(p_list) == 4:                       
                      self._tria_facet_lst.append(p_list[:])                       
                      p_list.clear()       
      except Exception as e:           
          raise RuntimeError(f"Error reading STL file: {e}")   

  def _triangle_properties(self, normal, v1, v2, v3):       
      """       
       Compute the area and volume contribution for one triangular facet.       
       Parameters       
       ----------       
       normal : array-like           
          Normal vector of the facet.       
       v1, v2, v3 : array-like           
          Vertices of the triangle.       
       Returns       
       -------       
       area : float           
          Area of the triangular facet.       
       volume : float           
          Volume contribution from this facet.       
       """       
      Normal = np.array(normal,dtype='f')       
      vertex1 = np.array(v1,dtype='f')       
      vertex2 = np.array(v2,dtype='f')       
      vertex3 = np.array(v3,dtype='f')       
      s1=np.linalg.norm(vertex2 - vertex1)       
      s2=np.linalg.norm(vertex3 - vertex2 )       
      s3=np.linalg.norm(vertex1 - vertex3)       
      # Semi-perimeter and Heron's formula for area       
      s=(s1+s2+s3)/2       
      ds = math.sqrt(s*((s-s1)*(s-s2)*(s-s3)))       
      vector_field = (vertex1 + vertex2 + vertex3 )/3       
      dv =(((vector_field[0]*Normal[0])+(vector_field[1]*Normal[1])+(vector_field[2]*Normal[2]))*ds)*(1/3)       
      return ds,dv     
     
  def compute(self):       
      """       
       Process all facets, compute total area and volume,        
       and update class attributes.       
       """       
      for i in self.tria_facets_getter :           
          tmp_area,tmp_vol = self._triangle_properties(i[0],i[1],i[2],i[3])           
          self.total_area += tmp_area           
          self.total_volume +=tmp_vol       
      return     

  def __str__(self):       
        """Return a formatted summary of the STL analysis results."""
        return (
            f"STL File: {self.File_path}\n"
            f"Total Surface Area: {self.total_area:.6f} mm²\n"
            f"Total Volume: {self.total_volume:.6f} mm³"
        )

  @property   
  def area (self):       
      """       
       Return the total surface area of the STL model.       
       Returns       
       -------       
       float           
          Total surface area in mm².       
       """     
      return(self.total_area)     

  @property   
  def volume(self):       
      """       
       Return the total volume of the STL model.       
       Returns       
       -------       
       float           
          Total volume in mm³.       
       """
      return(self.total_volume)

#usage 
if __name__ == "__main__":   
   stl_calc = STLAreaVolumeCalculator(r"C:\Users\saiba\Downloads\liver.stl")   
   # Access individual properties if needed   
   area = stl_calc.area   
   volume = stl_calc.volume
   print(stl_calc)
