import modules.architekten.func as architekten_func
import modules.interior_designer.func as interior_designer_func
import modules.innenarchitekten.func as innenarchitekten_func

if __name__ == "__main__":
    print("Scraping data for `architekten`")
    architekten_func.run()
    print("Scraping data for `interior_designer`")
    interior_designer_func.run()
    print("Scraping data for `innenarchitekten`")
    innenarchitekten_func.run()